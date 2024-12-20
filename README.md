# Phone Number Authentication API

## Описание проекта
Этот проект реализует API на Django и Django REST Framework (DRF) для авторизации пользователей по номеру телефона с последующей проверкой кода. Также поддерживается генерация и активация инвайт-кодов. API предоставляет следующие функции:

Авторизация по номеру телефона с проверкой 4-значного кода.

Автоматическое создание нового пользователя при первой 
авторизации.

Генерация уникального 6-значного инвайт-кода при первой авторизации.

Возможность ввода инвайт-кода другого пользователя.

Получение профиля пользователя и списка тех, кто использовал его инвайт-код.

## Установка
Клонируйте репозиторий:
```
bash
git clone <repository_url>
cd <repository_folder>
sudo docker compose -f docker-compose.yml up -d
```

## Эндпоинты
1. Авторизация по телефону
```
POST /api/users/register/
Описание: Отправка номера телефона и генерация кода.
Пример запроса:
json
{
  "phone": "+1234567890"
}
```
2. Проверка кода
```
POST /api/users/verify_code/
Описание: Проверка 4-значного кода для завершения авторизации.
Пример запроса:
json
{
  "phone": "+1234567890",
  "auth_code": "1234"
  "Token:" {
    "refresh": "...",
    "access": "..."
  }
}
```
3. Получение профиля
```
GET /api/users/me/
Описание: Возвращает информацию о текущем пользователе.
Пример ответа:
json
{
  "id": 1,
  "phone": "+1234567890",
  "invite_code": "ABC123",
  "activated_invite_code": "XYZ456",
  "users_invited": ["+9876543210"]
}
```
4. Обновление инвайт-кода
```
PATCH /api/profile/
Описание: Активация инвайт-кода другого пользователя.
Пример запроса:
json
{
  "invite_code": "XYZ456"
}
```
## Postman коллекция
Импортируйте Postman Collection из файла postman_collection.json, чтобы легко протестировать все доступные эндпоинты.

## Дополнительные опции
Документация API с использованием ReDoc доступна по адресу /redoc/

Django Templates

Docker: Подготовлен Dockerfile и docker-compose.yml для контейнеризации проекта.
Развертывание на Heroku или PythonAnywhere

### В связи того, что PythonAnywhere периодически отключает сервер, сайт может быть не доступен.
