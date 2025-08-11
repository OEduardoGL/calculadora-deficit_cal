from sqlalchemy import ForeignKey, String, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Calculation(Base):
    __tablename__ = "calculations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    payload: Mapped[dict] = mapped_column(JSON)      # entrada do cálculo (UserInput)
    result: Mapped[dict] = mapped_column(JSON)       # saída (NutritionResponse)
    objetivo: Mapped[str] = mapped_column(String(50))
    gcd: Mapped[int] = mapped_column(Integer)

    user = relationship("User", lazy="joined")
