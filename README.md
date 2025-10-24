# UGC Surveys

Сервис пользовательских опросов: создание опросов, прохождение, аналитика.

## Контакты

- Email: [krishtopadenis@gmail.com](mailto:krishtopadenis@gmail.com)
- Telegram: [@thefoxdk](https://t.me/thefoxdk)

## Демо-видео


## Стек

- Python 3.12, Django 5, DRF
- PostgreSQL, Docker Compose
- JWT (`djangorestframework-simplejwt`)
- OpenAPI (`drf-spectacular`)
- Типизация (`mypy`, `django-stubs`), линтинг (`ruff`)
- Пакетный менеджер — `uv`

## Структура

- `src/config` — настройки Django (`base`, `dev`, `prod`)
- `src/common` — базовые абстракции (`TimeStampedModel`)
- `src/users` — модели и API идентификаций
- `src/surveys` — домен опросов, сервисы и API

## Подготовка окружения

Скопируйте `.env.example` → `.env` и заполните переменные.

## Быстрый старт (Docker)

```bash
make build     # собрать образы
make up        # поднять web + db
make migrate   # применить миграции
```

Сервис будет доступен на `http://127.0.0.1:8000`.

## Полезные команды (Makefile)

- `make up` / `make down` — запустить/остановить проект
- `make restart` — пересобрать контейнер web
- `make reset` — остановить и удалить тома БД
- `make migrate` / `make makemigrations`
- `make shell` — Django shell внутри контейнера
- `make show_urls` — список URLов проекта
- `make lint` — `ruff check`
- `make format` — `ruff format`
- `make typecheck` — `mypy` со strict-настройками

## JWT аутентификация

1. `POST /api/v1/auth/register` — регистрация (email+password)
2. `POST /api/v1/auth/token` — получение access/refresh токенов
3. `POST /api/v1/auth/token/refresh` — обновление access токена
4. `POST /api/v1/auth/logout` — отзыв refresh (blacklist)

## Работа с опросами

- `GET /api/v1/surveys/list` — список опросов текущего автора
- `POST /api/v1/surveys/create` — создать опрос
- `GET /api/v1/surveys/{id}` — детальная информация (с вопросами и вариантами)
- `PATCH /api/v1/surveys/{id}` — обновление опроса и вложенных сущностей
- `DELETE /api/v1/surveys/{id}` — удаление (если нет ответов, иначе 409)
- CRUD для вопросов/вариантов: вложенные маршруты `questions/` и `options/`

## Прохождение опросов

- `GET /api/v1/surveys/{id}/runs/next-question` — получить очередной вопрос для пользователя
- `POST /api/v1/surveys/{id}/runs/answer` — отправить выбранный вариант
  - Завершение прогона → 204 и фиксация времени

## Статистика

`GET /api/v1/surveys/{id}/stats` — возвращает:

- total_runs
- avg_duration_seconds
- список вопросов с распределением ответов и топ-вариантом

## Качество кода

```bash
make lint
make typecheck
```

(Юнит-тесты будут добавлены позже.)

## OpenAPI/Swagger

- `GET /api/v1/schema` — JSON схема
- `GET /api/v1/docs` — Swagger UI
