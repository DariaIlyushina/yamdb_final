## YaMDb о проекте и авторах
Проект является агрегатором отзывов о фильмах, книгах и музыке

Авторы: Илюшина Дарья, Шурховецкий, Скрипкин Максим

## Установка

Клонируйте репозиторий с GitHub:
```
git clone https://github.com/DariaIlyushina/api_yamdb/
```

Перейдите в корневую директорию проекта, создайте и активируйте виртуальное окружение: 
```
$ python -m venv venv
...
$ source venv/Scripts/activate
```

Установите зависимости:
```
$ pip install requirements.txt
```

Запустите сервер разработчика:
```
$ python manage.py runserver
```
## Несколько примеров использования API
**GET /titles/** - получить список всех произведений  
Ответ (200):  
|Ключ|Значение|Описание|
|----|--------|--------|
|"id"|number|ID произведения|
|"name"|"string"|Название|
|"year"|number|Год выпуска|
|"rating"|number|Рейтинг произведения|
|"description"|"string"|Описание|
|"genre"|Array of objects|Жанр|
||"name"|Название жанра|
||"slug"|Поле "slug" |
|"category"|objects|Категория|
||"name"|Название категории объекта|
||"slug"|Поле "slug" |
  
**POST /auth/email/** - передача confirmation_code на адрес эл.почты  
Запрос:  
| Ключ |Значение|Описание|
| :--- |:------:|-------:|
| email|"string"|адрес эл.почты|

В результате, пользователь получает на указанный адрес эл.почты код подтверждения __confirmation_code__  

**PATCH /users/me/** - изменить данные своей учетной записи  
Запрос:  
| Ключ |Значение|Описание|
| :--- |:------:|-------:|
|"first_name"|"string"|Имя|
|"last_name"|"string"|Фамилия|
|"username"|"string"|Username|
|"bio"|"string"|О себе|
|"email"|"string"|Адрес электронной почты|
|"role"|"string"| Enum: "user" "moderator" "admin"|  

Ответ (200):
|Ключ|Значение|Описутмание|
|----|--------|--------|
|"first_name"|"string"|Имя|
|"last_name"|"string"|Фамилия|
|"username"|"string"|Username|
|"bio"|"string"|О себе|
|"email"|"string"|Адрес электронной почты|
|"role"|"string"| Enum: "user" "moderator" "admin"|

**

## Пример заполнения env

DB_ENGINE=django.db.backends.postgresql - указываем, что работаем с postgresql

DB_NAME=postgres - имя базы данных

POSTGRES_USER=postgres - логин для подключения к базе данных

POSTGRES_PASSWORD=postgres - пароль для подключения к БД (установите свой)

DB_HOST=db - название сервиса (контейнера)

DB_PORT=5432 - порт для подключения к БД 

## Запуск контейнера

cd infra/ - переходим в директорию

docker-compose up -d --build - запускаем контейнер

docker-compose exec web python manage.py migrate - делаем миграции

docker-compose exec web python manage.py createsuperuser - создаём супер пользователя

docker-compose exec web python manage.py collectstatic --no-input - подключем статику

## Копирование базы

docker-compose exec web python manage.py dumpdata > fixtures.json

## Наполнение БД fixtures

docker-compose exec web python manage.py loaddata <fixtures name>.json

## Cтатус вашего workflow.

После развертывания проект доступен по ссылке: http://localhost/

[![Django-app workflow](https://github.com/DariaIlyushina/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/DariaIlyushina/yamdb_final/actions/workflows/yamdb_workflow.yml)
