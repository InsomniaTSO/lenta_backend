# Инструкции по локальному запуску проекта LENTA BACKEND

## 1. Клонирование репозитория
Склонируйте репозиторий на ваш локальный компьютер:

`git clone git@github.com:InsomniaTSO/lenta_backend.git`


## 2. Переход в директорию проекта

`cd lenta_backend`
`cd backend`


## 3. Установка зависимостей

`pip install -r requirements.txt`


## 4. Применение миграций и загрузка тестовых данных. 

`python manage.py makemigrations categories`

`python manage.py makemigrations forecast`

`python manage.py makemigrations shops`

`python manage.py makemigrations users`

`python manage.py migrate`

`python manage.py load_shops`

`python manage.py load_cat`

`python manage.py load_sales`

`python manage.py load_forecast`


## 5. Создание суперпользователя

`python manage.py createsuperuser`


## 6. Запуск сервера

`python manage.py runserver`


## Ссылки

- Административная панель: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- API Endpoints:
  - Пользователи: [http://127.0.0.1:8000/api/v1/users/](http://127.0.0.1:8000/api/v1/users/)
  - Категории продуктов: [http://127.0.0.1:8000/api/v1/categories/](http://127.0.0.1:8000/api/v1/categories/)
  - Продажи: [http://127.0.0.1:8000/api/v1/sales/](http://127.0.0.1:8000/api/v1/sales/)
  - Магазины: [http://127.0.0.1:8000/api/v1/shops/](http://127.0.0.1:8000/api/v1/shops/)
  - Прогнозы: [http://127.0.0.1:8000/api/v1/forecast/](http://127.0.0.1:8000/api/v1/forecast/)
- Аутентификация:
  - Вход: [http://127.0.0.1:8000/api/auth/token/login/](http://127.0.0.1:8000/api/auth/token/login/)
  - Выход: [http://127.0.0.1:8000/api/auth/token/logout/](http://127.0.0.1:8000/api/auth/token/logout/)
- Документация:
  - Swagger UI: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
  - Redoc: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)
