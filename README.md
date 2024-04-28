# Описание проекта:
Спринт 14. Api для Yatube. Основная цель проекта - учебная практика. В ходе решения поставленной мне задачи я реализовал аутентификацию с помощью Djoser, модель Follow, включающую в себя ViewSet и Serializer, так же описал и остальные модели, требуемые в ТЗ.

# Как запустить проект:


Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

# Примеры:
### Отправка POST-запроса на подписку самого на себя:
```
http://127.0.0.1:8000/api/v1/follow/

Body:
{
    "following":"d2i3nns"
}
Answer 400:
{
    "non_field_errors": [
        "The fields user, following must make a unique set."
    ]
}
```
### Отправка GET-запроса с неаутентицфицированного пользователя
```
http://127.0.0.1:8000/api/v1/follow/

Body:
{
    "following":"admin"
}
Answer 400:
{
    "detail": "Authentication credentials were not provided."
}
```