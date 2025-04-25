# django-barter
# Как пользоваться

# 1. Установка проекта на VPS/VDS
Выберите хостинг, установите `Docker Engine` на виртуальный сервер по инструкции
https://docs.docker.com/engine/install/,
скопируйте проект на виртуальный сервер и перейдите в директорию проекта:
```
$ git clone https://github.com/Sheptor/django-barter.git
$ cd ./django-barter
```
Создайте суперпользователя, придумайте логин, пароль и укажите почту:
```
$ python3 ./manage.py createsuperuser
Имя пользователя (leave blank to use 'admin'): admin
Адрес электронной почты: example@example.example
Password: ********
Password (again): ********
Superuser created successfully.
```
Сделайте миграции базы данных, чтобы создать модели:
```
$ python3 ./manage.py makemigrations
$ python3 ./manage.py migrate
```
Создайте копию `.env.template` и переименуйте её в `.env`:
```
$ cp ./.env.template .env
```
# ВАЖНО!!! Держите SECRET_KEY в секрете, не храните его в открытом доступе
Сгенерируйте и скопируйте SECRET_KEY (необязательно, можно придумать свой)
```
$ python3 ./generate_secret_key.py
```

Задайте переменные окружения:
```
$ nano ./.env

  GNU nano 7.2                                                                           ./.env                                                                                    
SECRET_KEY=the_secret_key | вставьте сгенерированный или придуманный секретный ключ
DJANGO_LOGLEVEL=INFO | выберите один из (DEBUG, INFO, WARNING, ERROR, CRITICAL)
DJANGO_DEBUG=1 | 1 - ТОЛЬКО ДЛЯ РАЗРАБОТКИ, 0 - для продакшена
DJANGO_ALLOWED_HOSTS=example1.com,example2.ru,example3.ru | вставьте доступные домены сайта

# Чтобы сохранить ctrl+O, Enter,
# Чтобы закрыть nano ctrl+X
```
Проверьте работу приложения, запустив тесты:
```
$ python3 ./manage.py test ads
```
Соберите и запустите контейнер:
```
$ docker compose build
$ docker compose up
```