# API_YAMDB

### Описание проекта.
Данный проект выполняли:
Тимлид, разработчик №1: Демидов Юрий.
Разработчик №2: Лукашкин Илья.
Разработчик №3: Орлова Екатерина.

**Цель проекта** это обучение студента:
- работе в группе и выполнению заданий связанных друг с другом;
- работе с настройкой API-сервиса;
- созданию сложных REST API на базе проектов во фреймворке django;
- взаимодействию бэкенда и фронтенда;

**Задачи.**
В соответствии с техническим заданием(файл redoc.yaml) настроить работу библиотеки произведений.

### Установка проекта.
Как запустить проект:
1. Клонировать репозиторий и перейти в него в командной строке:

```git clone https://github.com/RV369/api_yamdb```

либо (в случае проблем с клонированием проекта) 
зайдя на страницу проекта нажать на кнопку 
Code -> Download ZIP и скачать проект в формате .zip
к себе на рабочую машину и открыть его.

2. Через терминал перейти в папку с проектом:

```cd api_yamdb```

3. Cоздать и активировать виртуальное окружение:

```python -m venv env```

```source venv/Scripts/activate```

4. Обновить версию pip(при необходимости) и установить зависимости из файла requirements.txt:

```python -m pip install --upgrade pip```

```pip install -r requirements.txt```

5. Установить и подключить библиотеку Simple JWT.

5.1. Установка библиотеки с помощью команды:

```pip install djangorestframework-simplejwt==5.1.0```

5.2. Подключение библиотеки в файле settings.py обязательно в указанном ниже порядке:

```INSTALLED_APPS = (```

```    'django.contrib.auth',```

...                   

```    'rest_framework',```

5.3. Добавление настроек к библиотеке в файле settings.py:

```from datetime import timedelta```

   ...

```REST_FRAMEWORK = {```

```    'DEFAULT_PERMISSION_CLASSES': [```

```        'rest_framework.permissions.IsAuthenticated',```

```],```

```'DEFAULT_AUTHENTICATION_CLASSES': [```

```    'rest_framework_simplejwt.authentication.JWTAuthentication',```

```],```

```}```

```SIMPLE_JWT = {```

```'ACCESS_TOKEN_LIFETIME': timedelta(days=1),```

```'AUTH_HEADER_TYPES': ('Bearer',),```

```}```

6. Перейти в рабочую папку и выполнить миграции:

```cd api_yamdb```

```python manage.py migrate```

7. Выполнить импорт всех необходимых данных из csv-файлов:

```python manage.py import start```

8. Запустить проект:

```python manage.py runserver```

### Примеры запросов API.
- GET-запрос по адресу /api/v1/titles/{title_id}
позволяет получить конкретное произведение.
- POST-запрос /api/v1/reviews
позволяет создать ревью к произведению
- DELETE-запрос по адресу /api/v1/comment/{id}/
позволяет удалить конкретный комментарий.
