import pandas as pd
import json
import os
from datetime import datetime

today = datetime.today().strftime('%d-%m-%Y')
filename = f'{today}_forecast.xlsx'
path_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname( __file__ ))), 'data/test_forecast.json')
path_file_xls = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname( __file__ ))), f'data/{filename}')
f = open(path_file)
forecasts = json.loads(f.read())['data']
forecast_pd = pd.DataFrame()
for forecast in forecasts:
    temp_forecast_pd = pd.DataFrame.from_dict(forecast)
    forecast_pd = forecast_pd._append(temp_forecast_pd)
forecast_pd['forecast_to_date'] = forecast_pd.index
forecast_pd = forecast_pd.loc[:,['store','sku','forecast_date', 'forecast_to_date', 'forecast']]
writer = pd.ExcelWriter(path_file_xls, engine='xlsxwriter')   
forecast_pd.to_excel(writer, sheet_name='forecast', index=False)
workbook  = writer.book
worksheet = writer.sheets['forecast']
worksheet.autofilter('A1:D1')
worksheet.set_column(0, 3, 30)
worksheet.set_column(4, 4, 10)
worksheet.write_formula('F2', '{=SUM(E2:E100)}')
chart = workbook.add_chart({'type': 'column'})
(max_row, max_col) = forecast_pd.shape
chart.add_series({'values': ['forecast', 5, 1, max_row+2, 1]})
worksheet.insert_chart(1, 3, chart)
writer.close()
print(forecast_pd.shape)