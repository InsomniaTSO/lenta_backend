import os
import requests
import logging
from datetime import date, timedelta
from api_host import API_HOST, API_PORT, API_VERSION 
from model import forecast

URL_CATEGORIES = 'categories'
URL_SALES = 'sales/ml_all'
URL_STORES = 'shops'
URL_FORECAST = 'forecast'


api_port = API_PORT 
api_host = API_HOST


_logger = logging.getLogger(__name__)


def setup_logging():

    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)
    handler_m = logging.StreamHandler()
    formatter_m = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
    handler_m.setFormatter(formatter_m)
    _logger.addHandler(handler_m) 


def get_address(resource):
    return f"http://{api_host}:{api_port}/api/{API_VERSION}/{resource}"


def get_stores():
    url = get_address(URL_STORES) 
    response = requests.get(url)
    if response.status_code != 200:
        _logger.warning('Сервер недоступен. Неудалось получить список магазинов.')
        return []
    return response.json()['data']


def get_categories():
    url = get_address(URL_CATEGORIES)
    response = requests.get(url)
    if response.status_code != 200:
        _logger.warning('Сервер недоступен. Неудалось получить список категорий.')
        return {}
    
    result = {el['sku']: el for el in response.json()['data']}
    return result


def get_sales():
    url = get_address(URL_SALES)
    response = requests.get(url)
    if response.status_code != 200:
        _logger.warning('Сервер недоступен. Неудалось получить историю продаж.')
    return response.json()['data'][1:10]


def main(today=date.today()):
    forecast_dates = [today + timedelta(days=d) for d in range(1, 14)]
    forecast_dates = [el.strftime('%Y-%m-%d') for el in forecast_dates]
    categories = get_categories()
    for store in get_stores():
        result = []
        for sale in get_sales():
            sale_info = categories[sale['sku']]
            sales = sale['fact']
            prediction = forecast(store, sales, sale_info)
            result.append({'store': store['store'],
                           'forecast_date': today.strftime('%Y-%m-%d'),
                           'forecast': {'sku': sale['sku'],
                                        'sales_units': {k: v for k, v in zip(forecast_dates, prediction)}
                                        }
                          })
        print(result)
        requests.post(get_address(URL_FORECAST), json=result)  


if __name__ == '__main__':
    setup_logging()
    main()

