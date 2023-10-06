import os
from pathlib import Path
import pickle
import pandas as pd
import tensorflow as tf

from datetime import date, timedelta 
from keras.models import load_model
from keras.utils import get_custom_objects

FILE_PATH = Path(__file__).parents[0] / 'models'

data_holidays = pd.read_csv(os.path.join(FILE_PATH, 'holidays_covid_calendar.csv'), parse_dates=[4])
data_holidays = data_holidays.drop(['year', 'day', 'weekday', 'covid'], axis=1)

def wape(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float32)
    error = tf.abs(y_true - y_pred)
    denominator = tf.abs(y_true) + tf.abs(y_pred)
    return tf.reduce_sum(error) / tf.reduce_sum(denominator)

model = load_model(os.path.join(FILE_PATH, 'lstm-model.h5'), custom_objects={'wape': wape})
enc = pickle.load(open(os.path.join(FILE_PATH, 'ordinal_encoder.sav'), 'rb'))
scaler = pickle.load(open(os.path.join(FILE_PATH, 'min_max_scaler.sav'), 'rb'))
     
def forecast(store, sale, sale_info, date=date):
        
    today = date.today()        
    forecast_dates = [today + timedelta(days=d) for d in range(1, 15)]
    forecast_dates = [el.strftime('%Y-%m-%d') for el in forecast_dates]

    data = pd.DataFrame({}, columns=['st_id', 'pr_sku_id', 'pr_sales_type_id', 'pr_uom_id', 'day', 'weekday', 'date']) 
    rows = {}
    i = 0
    for date in forecast_dates:
        data.loc[i] = [store['store'], sale_info['sku'], 0, 0, 0, 0, date]
        i += 1
               
             
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    dates = data['date'].copy()
    data = pd.merge(data, data_holidays, left_on='date', right_on='calday')
          
            
    data_params = data[~data['pr_sku_id'].duplicated()]

    for index, row in data_params.iterrows():
        filter = (data['pr_sku_id'] == row['pr_sku_id'])
        data.loc[filter, 'pr_sales_type_id'] = row['pr_sales_type_id']
        data.loc[filter, 'pr_uom_id'] = row['pr_uom_id']

    data['day'] = data['date_x'].dt.day
    data['weekday'] = data['date_x'].dt.weekday
    data['month'] = data['date_x'].dt.month 
    data['quarter'] = pd.PeriodIndex(data['date_x'], freq='Q')

    data = data.drop(['date_x', 'date_y', 'calday'], axis=1)   
            
    columns = ['st_id', 'pr_sku_id', 'quarter']
    data[columns] = enc.transform(data[columns])
    data = scaler.transform(data)
    y_preds = pd.DataFrame(model.predict(data).round().astype('int'))
            
    result = pd.concat([dates, y_preds[0]], axis=1)
    response = {}
    for index, row in result.iterrows():
        response[row['date'].strftime('%Y-%m-%d')] = row[0]
    return response
  
