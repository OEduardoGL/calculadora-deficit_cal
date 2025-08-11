from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.auth import UserCreate, Token
from app.repositories import user_repo

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if user_repo.get_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email já registrado")
    user_repo.create(db, email=data.email, hashed_password=get_password_hash(data.password))
    return {"message": "registrado com sucesso"}

@router.post("/login", response_model=Token)
def login(data: UserCreate, db: Session = Depends(get_db)):
    user = user_repo.get_by_email(db, data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    token = create_access_token(user.email)
    return {"access_token": token}
