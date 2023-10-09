import os
from dotenv import load_dotenv
import json
import requests
import logging
from datetime import date, timedelta
from api_host import API_HOST, API_PORT, API_VERSION

load_dotenv()

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from model import forecast

URL_CATEGORIES = "categories"
URL_SALES = "sales/ml_all"
URL_STORES = "shops"
URL_FORECAST = "forecast"
DS_USER = os.getenv('DS_USER')
DS_PASSWORD=os.getenv('DS_PASSWORD')

_logger = logging.getLogger(__name__)

def setup_logging():

    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)
    handler_m = logging.StreamHandler()
    formatter_m = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler_m.setFormatter(formatter_m)
    _logger.addHandler(handler_m) 


def get_auth_token(login, password):
    headers = {"Content-type": "application/json"}
    login_param = {"password": password, "email": login}
    token = requests.post(f"http://{API_HOST}:{API_PORT}/api/auth/token/login/", 
                          json.dumps(login_param), 
                          headers=headers)
    if token.status_code != 201:
        _logger.warning(f"Сервер недоступен. {token.status_code}")
    else:
        return token.json()["auth_token"]


def get_address(resource):
    token = get_auth_token(DS_USER, DS_PASSWORD)
    url = f"http://{API_HOST}:{API_PORT}/api/{API_VERSION}/{resource}/"
    return url, token


def get_stores():
    url, token = get_address(URL_STORES)
    headers = {"Authorization": f"Token {token}"} 
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        _logger.warning("Сервер недоступен. Неудалось получить список магазинов.")
        return []
    return response.json()["data"][0:1]


def get_categories():
    url, token = get_address(URL_CATEGORIES)
    headers = {"Authorization": f"Token {token}"} 
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        _logger.warning(f"Сервер недоступен. Неудалось получить список категорий. {response.status_code}")
        return {}
    result = {el["sku"]: el for el in response.json()["data"]}
    return result


def get_sales(store=None, sku=None):
    url, token = get_address(URL_SALES)
    headers = {"Authorization": f"Token {token}"}
    params = {}
    if store is not None:
        params["store"] = store
    if sku is not None:
        params["sku"] = sku
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        _logger.warning("Сервер недоступен. Неудалось получить историю продаж.")
    return response.json()["data"][0:1]


def main(today=date.today()):

    forecast_dates = [today + timedelta(days=d) for d in range(1, 14)]
    forecast_dates = [el.strftime("%Y-%m-%d") for el in forecast_dates]
    categories = get_categories()
    for store in get_stores():  
        result = []
        for sale in get_sales(store=["store"]):
            sale_info = categories[sale["sku"]]
            sales = sale["fact"]
            prediction = forecast(store, sales, sale_info)
            result.append({"store": store["store"],
                           "forecast_date": today.strftime("%Y-%m-%d"),
                           "forecast": {"sku": sale["sku"],
                                        "sales_units":prediction
                                        }
                          })
        url, token = get_address(URL_FORECAST)
        headers = {"Content-type": "application/json",
                   "Authorization": f"Token {token}"}
        result_d = {"data": json.dumps(result)}
        response = requests.post(url, result_d, headers=headers)
    if response.status_code == 201:
        _logger.info(f"Прогноз успешно загружен. {today.strftime('%Y-%m-%d')}") 
    else:
        _logger.info(f"Ошибка при загрузке прогноза. {response.status_code}") 
        print(response)


if __name__ == "__main__":
    setup_logging()
    main()

