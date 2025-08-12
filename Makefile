DC := $(shell if docker compose version >/dev/null 2>&1; then echo "docker compose"; \
             elif docker-compose --version >/dev/null 2>&1; then echo "docker-compose"; \
             else echo "COMPOSE_NOT_FOUND"; fi)

ifeq ($(DC),COMPOSE_NOT_FOUND)
$(error Docker Compose não encontrado. Instale o plugin 'docker compose' ou o binário 'docker-compose'.)
endif

.PHONY: up down logs api bash db

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
