## Проект YaMDb собирает отзывы пользователей на произведения.

предоставляет API интерфейс основанный на Django REST framework. Позволяет: 
```
создать, просмотривать, редактировать:
- данные о произведениях,
- категории и жанры произведений,
- отзывы и комментарии на произведения.
создавать и управлять пользователями, гибко ограничивать доступность ресуров
на основе разделений полномочий(используется JWT токены).
```

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Egor-junior/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

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

Ознакомиться с документацией проекта можно по адресу:

```
http://127.0.0.1:8000/redoc/
```

### Для реализации использовались следующие технологии:

```
- Django REST framework
```

### Примеры запросов:

**GET** api/v1/titles/
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```

**POST** api/v1/users/
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

**GET** /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
... 
```
для более полной информации обратитесь к документации
```

