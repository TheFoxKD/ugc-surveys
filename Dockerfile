# Базовый образ с установленным uv и Python 3.12
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Рабочая директория приложения внутри контейнера
WORKDIR /app

# Копируем весь проект и устанавливаем зависимости из uv.lock
COPY . /app
RUN uv sync --locked

# Добавляем бинарники виртуального окружения в PATH
ENV PATH="/app/.venv/bin:$PATH"

# Публикуем порт
EXPOSE 8000

# Запуск сервера
CMD ["python", "-m", "src.manage", "runserver", "0.0.0.0:8000"]
