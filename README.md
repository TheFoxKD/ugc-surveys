# UGC Surveys

Сервис пользовательских опросов: создание опросов, прохождение, аналитика.

## Контакты

- Email: [krishtopadenis@gmail.com](mailto:krishtopadenis@gmail.com)
- Telegram: [@thefoxdk](https://t.me/thefoxdk)

## Демо-видео

[Demo Video](https://github.com/user-attachments/assets/18b1969c-8d58-49fc-b7a9-ce52b1c964cb)

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

## Команды (Makefile)

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

## Права доступа и роли

- **Кто может создавать опросы**: любой аутентифицированный пользователь (JWT).
- **Кто видит/редактирует/удаляет свой опрос**: только автор опроса.
  - Реализовано через `IsSurveyAuthor` на detail/статистике; список (`/surveys/list`) фильтруется по текущему пользователю.
- **Кто может проходить опросы**: любой аутентифицированный пользователь (не только автор).
- **Удаление с ответами**: если по опросу уже есть ответы, удаление отклоняется (вернётся 400).

Таким образом, автор управляет только своими опросами и видит их статистику, а остальные пользователи могут их проходить, но не модифицировать.

## Работа с опросами

- `GET /api/v1/surveys/list` — список опросов текущего автора
- `POST /api/v1/surveys/create` — создать опрос
- `GET /api/v1/surveys/{id}` — детальная информация (с вопросами и вариантами)
- `PATCH /api/v1/surveys/{id}` — обновление опроса и вложенных сущностей
- `DELETE /api/v1/surveys/{id}` — удаление (если нет ответов, иначе 409)
- CRUD для вопросов/вариантов: вложенные маршруты `questions/` и `options/`

## Прохождение опросов

- `GET /api/v1/surveys/{id}/runs/next-question` — получить очередной вопрос для пользователя
  - Ответ 200: `{ run_id, question }`
  - Если вопросов больше нет: 204 (прогон помечается завершённым)
- `POST /api/v1/surveys/{id}/runs/answer` — отправить выбранный вариант
  - Ответ 200: `{ run_id, completed, question|null }`
    - `completed=false` и заполненный `question` — есть следующий вопрос
    - `completed=true` и `question=null` — опрос завершён, время зафиксировано

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

## OpenAPI/Swagger

- `GET /api/v1/schema` — JSON схема
- `GET /api/v1/docs` — Swagger UI
