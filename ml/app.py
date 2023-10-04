import schedule
import threading
import requests
import logging
from datetime import date, timedelta
from api_host import API_HOST, API_PORT, API_VERSION 
import random

URL_CATEGORIES = 'categories'
URL_SALES = 'sales/ml_all'
URL_STORES = 'shops'
URL_FORECAST = 'forecast'


api_port = API_PORT 
api_host = API_HOST


_logger = logging.getLogger(__name__)

def run_continuously():
    cease_continuous_run = threading.Event()
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def setup_logging():

    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)
    handler_m = logging.StreamHandler()
    formatter_m = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
    handler_m.setFormatter(formatter_m)
    _logger.addHandler(handler_m) 


def get_address(resource):
    return f"http://{api_host}:{api_port}/api/{API_VERSION}/{resource}/"


def get_stores():
    url = get_address(URL_STORES) 
    response = requests.get(url)
    if response.status_code != 200:
        _logger.warning('Сервер недоступен. Неудалось получить список магазинов.')
        return []
    return response.json()['data'][0:2]


def get_categories():
    url = get_address(URL_CATEGORIES)
    response = requests.get(url)
    if response.status_code != 200:
        _logger.warning('Сервер недоступен. Неудалось получить список категорий.')
        return {}
    return response.json()['data'][0:2]


def get_sales():
    url = get_address(URL_SALES)
    response = requests.get(url)
    if response.status_code != 200:
        _logger.warning('Сервер недоступен. Неудалось получить историю продаж.')
    return response.json()['data']


def main(today=date.today()):
    forecast_dates = [today + timedelta(days=d) for d in range(0, 13)]
    forecast_dates = [el.strftime('%Y-%m-%d') for el in forecast_dates]
    categories = get_categories()
    stores = get_stores()
    result = dict()
    result_list = []
    for store in stores:
        for sku in categories:
            result['store'] = store['store']
            result['forecast_date'] = today.strftime('%Y-%m-%d')
            result['forecast'] = dict()
            result['forecast']['sku']= sku['sku']
            result['forecast']['sales_units']= dict()
            for date in forecast_dates:
                result['forecast']['sales_units'][date] = random.randint(1, 20)
            result_list.append(result)
            result = dict()
    headers = {'Content-type': 'application/json'}
    response = requests.post(get_address(URL_FORECAST), 
                      json={"data" : result_list}, 
                      headers=headers)
    if response.status_code != 200:
        _logger.info(f'Прогноз успешно загружен. {today.strftime("%Y-%m-%d")}')
    

if __name__ == '__main__':
    setup_logging()
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main - starting thread")
    # schedule.every().day.do(main())
    schedule.every().minute.do(main)
    stop_run_continuously = run_continuously()
    stop_run_continuously.set()