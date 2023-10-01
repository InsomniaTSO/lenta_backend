import os
import pickle
import pandas as pd

model = None
file_name = 'model.pkl'
file_model = os.path.join('', file_name)
def forecast(store, sale, sale_info):
    """
    :params store: 
    {'store': 'asd1', 'city': 'erert', 'division': 'tuy5r', 'type_format': 1, 'loc': 3, 'size': 19, 'is_active': 0}
    :params sale: 
    [{'date': '2023-01-15', 'sales_type': 0, 'sales_units': 5, 'sales_units_promo': 4, 'sales_rub': 6.7, 'sales_run_promo': 8.9}, 
    {'date': '2023-01-16', 'sales_type': 0, 'sales_units': 2, 'sales_units_promo': 6, 'sales_rub': 9.6, 'sales_run_promo': 3.4}]
    :params sale_info 2:
    {'sku': 'sku1', 'group': 'dfsdf', 'category': 'sdfsdf', 'subcategory': 'sdfdfs', 'uom': 1}
    :return: ["2023-09-01": 1]

    """
    if os.path.isfile(file_model):
        model = pickle.load(open(file_name, 'rb'))
        #X_test = pd.DataFrame([store, sale, sale_info],columns=['st_id', 'pr_sku_id', 'date'])
        #prediction = model.predict(X_test)
    prediction = ''
    return prediction