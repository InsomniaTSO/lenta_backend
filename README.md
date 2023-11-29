# __Проект «Хакатон Лента»__

## __Описание__:
Мастерская Яндекс Практикума (октябрь 2023 г.)
Проектное участие в кросс-функциональном хакатоне по разработке ML-продукта и 
интерфейса предсказательной модели для ООО “Лента”. 

## __Цель проекта__:  
Разработка вэб-сервиса, позволяющего видеть прогноз спроса на 14 дней для товаров 
собственного производства заказчика. Необходимо было создать ML библиотеку и API к ней 
и вывести эти данные в интерфейс.

## __Авторы backend части__:
Татьяна Манакова.
Валентина Кириленко.

## __Технологии backend части__:

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Django REST framework](https://www.django-rest-framework.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)
* [Gunicorn](https://gunicorn.org/)
* [Nginx](https://nginx.org/)

## __Подготовка и запуск проекта__:

* Клонируйте репозиторий:

```
git clone git@github.com:InsomniaTSO/lenta_backend.git
```

* На сервере установите Docker и docker-compose:

```
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

* Заполните .env по шаблону

* На сервере соберите запустите контейнеры:

из папки backend:
```
docker build -t lenta_backend .
docker tag lenta_backend:latest lenta_backend:staging

```

из папки ds:
```
docker build -t ml .
docker tag ml:latest ml:staging

```

из папки infra:
```
docker-compose up

```

Загрузка тестовых данных из папки "data":
```
python manage.py load_shops [file_name]&&
python manage.py load_cat [file_name]&&
python manage.py load_sales [file_name]&&
python manage.py load_forecast [file_name]&&
```


создание createsuperuser:
```
docker exec -it infra-backend-1 python manage.py createsuperuser

```

### __Шаблон наполнения env-файла__:

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=xxxxxx # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxx # секретный ключ из settings.py
DS_USER=123@123.com # логин для подключения к ml модели к бекэнду
DS_PASSWORD=xxxxxx # пароль для подключения к ml модели к бекэнду
```

## Структура проекта:

- Административная панель: [http://localhost/admin/](http://localhost/admin/)
- API Endpoints:
  - Пользователи: [http://localhost/api/v1/users/](http://localhost/api/v1/users/)
  - Категории продуктов: [http://localhost/api/v1/categories/](http://localhost/api/v1/categories/)
  - Продажи: [http://localhost/api/v1/sales/](http://localhost/api/v1/sales/)
  - Магазины: [http://localhost/api/v1/shops/](http://localhost/api/v1/shops/)
  - Прогнозы: [http://localhost/api/v1/forecast/](http://localhost/api/v1/forecast/)
  - Скачать прогноз: [http://localhost/api/v1/forecast/](http://localhost/api/v1/forecast/)
- Аутентификация:
  - Вход: [http://localhost/api/auth/token/login/](http://localhost/api/auth/token/login/)
  - Выход: [http://localhost/api/auth/token/logout/](http://localhost/api/auth/token/logout/)
- Документация:
  - Swagger UI: [http://localhost/api/docs/](http://localhost/api/docs/)
  - JSON-схема API: [http://localhost/api/schema/](http://localhost/api/schema/)