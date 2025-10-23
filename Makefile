.PHONY: up down migrate makemigrations shell lint typecheck test local build restart reset


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

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy src
