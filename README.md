# Calculadora de Dieta — API FastAPI

## Descrição

API REST em **FastAPI** que calcula **necessidade calórica** (TMB/TDEE) e **macronutrientes** a partir de dados do usuário, considerando o objetivo (déficit, manutenção com ganho, ou bulking limpo).

A API possui **autenticação JWT**, **salva cálculos por usuário** e expõe **histórico**. Está **dockerizada** com **PostgreSQL** e **pgAdmin**, e pode ser executada tanto localmente (uvicorn) quanto via Docker/Compose.

## Objetivos

- Calcular TMB (Mifflin-St Jeor) e TDEE por nível de atividade
- Ajustar calorias/macros por objetivo:
  - **Déficit** (perder gordura com alta proteína)
  - **Manutenção** com ganho de massa
  - **Superávit** (bulking limpo)
- Autenticação segura e controle de acesso por usuário
- Persistência e listagem de **histórico de cálculos**

## Tecnologias e Ferramentas

| Ferramenta | Para que serve |
|---|---|
| **FastAPI** | Framework da API (tipagem, validação, docs automáticas) |
| **Uvicorn** | Servidor ASGI |
| **Pydantic + Settings** | Validação de dados e gerenciamento de variáveis de ambiente |
| **SQLAlchemy (2.x)** | ORM e acesso ao banco |
| **PostgreSQL** | Banco de dados relacional (em Docker) |
| **JWT (python-jose)** | Autenticação baseada em tokens |
| **Passlib[bcrypt]** | Hash de senhas |
| **Pytest** | Testes automatizados |
| **Alembic** | Migrations para versionamento e controle do schema do banco |
| **Docker / Docker Compose** | Empacotar e orquestrar API + DB + pgAdmin |
| **pgAdmin** | GUI web para o PostgreSQL |
| **Makefile** | Atalhos para subir/descer serviços rapidamente |

## Estrutura do Projeto

```
├── app/                     # código da API
│   ├── api/v1/endpoints/    # rotas (auth, nutrition)
│   ├── core/                # config, segurança, startup
│   ├── db/                  # models, session, base
│   ├── repositories/        # acesso ao banco
│   └── schemas/             # Pydantic (requests/responses)
├── tests/                   # testes (pytest)
├── alembic/                 # migrations do banco (controladas pelo Alembic)
├── alembic.ini              # config do Alembic
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── .env                     # (para Docker/Compose) -> gerar a partir de .env.docker.example
├── .env.app                 # (para rodar local) -> gerar a partir de .env.example
├── .env.docker.example      # exemplo para Docker/Compose
└── .env.example             # exemplo para rodar local (uvicorn)
```

> **Importante sobre `.env`**
>
> - Para **rodar local (uvicorn)**, use **`.env.app`** (criado a partir de `.env.example`)
> - Para **rodar com Docker/Compose**, use **`.env`** (criado a partir de `.env.docker.example`)
> - Os arquivos `*.example` **podem** ser versionados; os `.env` reais **não**

## Como Rodar

### Opção 1: Local (uvicorn)

1. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate   # Windows
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente:**
   - Crie `.env.app` a partir de `.env.example`
   - Gere uma `SECRET_KEY` forte:
     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(64))"
     ```

4. **Execute a API:**
   ```bash
   uvicorn app.main:app --reload
   ```

**Acesse:** http://127.0.0.1:8000

> **Dica:** Para usar **PostgreSQL** local, garanta que há um servidor rodando e que `DATABASE_URL` aponta corretamente.
> Para testes rápidos com **SQLite**, defina:
> ```env
> DATABASE_URL=sqlite:///./app.db
> ```

### Opção 2: Docker/Compose (API + Postgres + pgAdmin)

1. **Crie `.env` a partir de `.env.docker.example`:**
   ```env
   # .env (exemplo para Compose)
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=calcalc
   DB_PORT=5432               # use 5433 se 5432 já estiver em uso no host

   SECRET_KEY=coloque-uma-chave-forte
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   BACKEND_CORS_ORIGINS=http://localhost:5173,http://localhost:3000

   PGADMIN_DEFAULT_EMAIL=admin@local
   PGADMIN_DEFAULT_PASSWORD=admin
   ```

2. **Gere a `SECRET_KEY` como mostrado acima**

3. **Suba todos os serviços:**
   ```bash
   make up
   # ou: docker-compose up --build -d
   ```

### URLs de Acesso

- **API:** http://127.0.0.1:8000
- **Documentação:** http://127.0.0.1:8000/docs
- **pgAdmin:** http://127.0.0.1:5050
  - **Login:** `admin@local` / `admin`
  - **Para conectar ao banco:** Host: `db`, Port: `5432`, User/Pass conforme `.env`

### Comandos Úteis

- **Ver logs da API:** `make logs`
- **Parar serviços:** `make down`

## Testes

Os testes de integração foram implementados com **pytest**, cobrindo:
- Registro e login de usuários
- Fluxo completo de salvar cálculos e consultar histórico

### Rodar todos os testes
```bash
make test
# ou
pytest -q
```

### Migrations (Alembic)

Para aplicar as migrations (criar/atualizar tabelas no banco):

```bash
# Gerar uma nova migration automaticamente
alembic revision --autogenerate -m "mensagem da mudança"

# Aplicar migrations
alembic upgrade head

# Reverter última migration
alembic downgrade -1
```

## Endpoints Principais

### Autenticação

- `POST /api/v1/auth/signup` — Criar usuário
- `POST /api/v1/auth/login` — Fazer login (retorna `access_token`)

### Cálculos Nutricionais

- `POST /api/v1/nutrition/calculate` — Cálculo público (sem salvar)
- `POST /api/v1/nutrition/save` — Salvar cálculo (requer autenticação)
- `GET /api/v1/nutrition/history?skip=0&limit=10` — Histórico (requer autenticação)

## Documentação Interativa

- **Swagger UI:** http://127.0.0.1:8000/docs
- **Redoc:** http://127.0.0.1:8000/redoc

## Testes Rápidos (curl)

### Criar usuário
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"dev@ex.com","password":"segredo123"}'
```

### Fazer login
```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"dev@ex.com","password":"segredo123"}' | jq -r .access_token)
```

### Calcular (endpoint público)
```bash
curl -X POST http://127.0.0.1:8000/api/v1/nutrition/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "sexo":"M",
    "peso":80,
    "altura":180,
    "idade":28,
    "fator_atividade":"moderadamente_ativo",
    "objetivo":"perder_gordura"
  }'
```

### Salvar no histórico (requer autenticação)
```bash
curl -X POST http://127.0.0.1:8000/api/v1/nutrition/save \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sexo":"M",
    "peso":80,
    "altura":180,
    "idade":28,
    "fator_atividade":"moderadamente_ativo",
    "objetivo":"perder_gordura"
  }'
```

### Listar histórico (requer autenticação)
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/nutrition/history?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```
