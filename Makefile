.PHONY: up down migrate makemigrations shell lint typecheck test local build restart reset show_urls


build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose up -d --force-recreate

reset:
	docker compose down -v

migrate:
	docker compose exec web uv run python -m src.manage migrate

makemigrations:
	docker compose exec web uv run python -m src.manage makemigrations

shell:
	docker compose exec web uv run python -m src.manage shell

show_urls:
	docker compose exec web uv run python -m src.manage show_urls

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	PYTHONPATH=src DJANGO_SETTINGS_MODULE=config.settings.dev uv run mypy src
