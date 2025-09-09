from sqlalchemy.orm import Session

from app.db.models.calculation import Calculation


def create(
    db: Session, *, user_id: int, payload: dict, result: dict, objetivo: str, gcd: int
) -> Calculation:
    c = Calculation(
        user_id=user_id, payload=payload, result=result, objetivo=objetivo, gcd=gcd
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


def list_by_user(
    db: Session, user_id: int, *, skip: int = 0, limit: int = 20
) -> list[Calculation]:
    return (
        db.query(Calculation)
        .filter(Calculation.user_id == user_id)
        .order_by(Calculation.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
