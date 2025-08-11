# 🥗 Calculadora de Dieta — API FastAPI

## 📌 Descrição
Esta aplicação é uma **API REST** desenvolvida com **FastAPI** que calcula a **necessidade calórica e distribuição de macronutrientes** com base em dados fornecidos pelo usuário, considerando seu objetivo (perder gordura, manter massa muscular ou bulking limpo).  
O sistema também implementa **autenticação com JWT**, salvamento de cálculos por usuário e histórico consultável, permitindo que o usuário acompanhe sua evolução.

---

## 🎯 Objetivos da Aplicação
- Calcular **TDEE** (Total Daily Energy Expenditure) e macronutrientes personalizados.
- Adaptar cálculos de acordo com o **objetivo do usuário**:
  - 🔻 Déficit calórico (perda de gordura)
  - ⚖️ Manutenção com ganho muscular
  - 🔺 Superávit calórico (bulking limpo)
- Permitir **cadastro e login seguro**.
- Salvar os cálculos no **histórico do usuário**.
- Retornar dados via **endpoints REST** prontos para integração com front-end.

---

## 🛠 Tecnologias e Ferramentas
| Ferramenta / Biblioteca | Uso no Projeto |
|------------------------|----------------|
| **FastAPI** | Framework principal para criação da API. |
| **Uvicorn** | Servidor ASGI para rodar a aplicação FastAPI. |
| **Pydantic** | Validação de dados e tipagem forte para as requisições e respostas. |
| **Pydantic Settings** | Gerenciamento de variáveis de ambiente e configurações. |
| **SQLite** | Banco de dados relacional simples para armazenamento local. |
| **SQLAlchemy** | ORM para modelagem e persistência dos dados no banco. |
| **JWT (JSON Web Token)** | Autenticação e controle de acesso seguro. |
| **Passlib** | Criptografia de senhas dos usuários. |
| **Pytest** | Testes automatizados para endpoints e regras de negócio. |

---

## 🚀 Como Rodar o Projeto Localmente
### Criar e ativar ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# ou
.venv\Scripts\activate      # Windows
```
### Instalar dependências
```bash
pip install -r requirements.txt
```
### Configurar variáveis de ambiente
```bash
Crie um arquivo .env na raiz do projeto com base no .env.example
```
### Rodar a API
```bash
uvicorn app.main:app --reload
```
## 📡 Endpoints Principais

### 🔑 Autenticação
- **POST** `/api/v1/auth/signup` → Criar nova conta.  
- **POST** `/api/v1/auth/login` → Obter token JWT.

### 🥗 Cálculos
- **POST** `/api/v1/nutrition/save` → Salvar cálculo no histórico (**autenticado**).  
- **GET** `/api/v1/nutrition/history` → Consultar histórico do usuário (**autenticado**).

---

## 📄 Documentação Interativa
Após iniciar o servidor, acesse:
- **Swagger UI** → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **Redoc** → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Testes
Para rodar os testes automatizados:
```bash
pytest
```