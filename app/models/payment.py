from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.db.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="processing")