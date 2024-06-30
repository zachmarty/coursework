# Бэк часть для доски объявлений

## Описание проекта

В данном проекте реализована бэк составляющая доски объявлений

# Подготовка

- установить проект
- создать и активировать виртуальное окружение python -m venv venv
- установить зависимости pip install -r requirements.txt
- создать базу данных в postgresql
- создать файл виртуальных окружений skymarket/.env и заполнить его по образцу .env.example
- применить миграции python skymarket/manage.py migrate
- запустить сервер python skymarket/manage.py runserver

## API

Документация по работе с api находится по адресу /swagger или /redoc

## Docker

Для запуска приложения в docker использовать команды docker-compose build и docker-compose up