# CalCalc API 

## Requisitos
- Python 3.11+
- pip

## Instalação
```bash
python -m venv .venv
# linux/mac
source .venv/bin/activate
# windows
# .venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload
