from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_admin
from app.db.database import get_db
from app.models.claim import Claim
from app.models.payment import Payment
from app.models.user import User

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("/")
def get_my_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payments = (
        db.query(Payment)
        .join(Claim, Payment.claim_id == Claim.id)
        .filter(Claim.user_id == current_user.id)
        .order_by(Payment.id.desc())
        .all()
    )
    return payments


@router.get("/all")
def get_all_payments(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    payments = db.query(Payment).order_by(Payment.id.desc()).all()
    return payments