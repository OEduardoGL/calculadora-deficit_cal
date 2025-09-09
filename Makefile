DC := $(shell if docker compose version >/dev/null 2>&1; then echo "docker compose"; \
             elif docker-compose --version >/dev/null 2>&1; then echo "docker-compose"; \
             else echo "COMPOSE_NOT_FOUND"; fi)

ifeq ($(DC),COMPOSE_NOT_FOUND)
$(error Docker Compose não encontrado. Instale o plugin 'docker compose' ou o binário 'docker-compose'.)
endif

.PHONY: up down logs api bash db \
        migrate revision current history downgrade \
        ps rebuild restart \
        lint format format-check pre-commit-install pre-commit-run

up:
	$(DC) up --build -d

down:
	$(DC) down

logs:
	$(DC) logs -f api

bash:
	docker exec -it calcalc-api bash

db:
	docker exec -it calcalc-db psql -U $${POSTGRES_USER:-postgres} -d $${POSTGRES_DB:-calcalc}

api:
	curl -s http://127.0.0.1:8000/ | jq

ps:
	$(DC) ps

rebuild:
	$(DC) build api

restart:
	$(DC) restart api

migrate:
	$(DC) exec api bash -lc 'PYTHONPATH=. alembic upgrade head'

revision:
	@if [ -z "$(msg)" ]; then echo "Use: make revision msg=\"sua mensagem\""; exit 1; fi
	$(DC) exec api bash -lc 'PYTHONPATH=. alembic revision -m "$(msg)" --autogenerate'

current:
	$(DC) exec api bash -lc 'PYTHONPATH=. alembic current'

history:
	$(DC) exec api bash -lc 'PYTHONPATH=. alembic history'
downgrade:
	@if [ -z "$(rev)" ]; then echo "Use: make downgrade rev=-1  (ou rev=<rev_id>/base/head)"; exit 1; fi
	$(DC) exec api bash -lc 'PYTHONPATH=. alembic downgrade $(rev)'

.PHONY: test test-verbose cov

test:
	PYTHONPATH=. pytest -q

test-verbose:
	pytest -vv

cov:
	pytest --maxfail=1 --disable-warnings -q --cov=app --cov-report=term-missing

# --- Quality ---

lint:
	ruff check .
	black --check .

format:
	ruff check --fix .
	black .

format-check:
	ruff check .
	black --check .

pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files
