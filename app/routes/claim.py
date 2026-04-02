import logging
import time

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_admin
from app.db.database import SessionLocal, get_db
from app.models.claim import Claim
from app.models.payment import Payment
from app.models.user import User

router = APIRouter(prefix="/claims", tags=["Claims"])
logger = logging.getLogger(__name__)


def process_payment(payment_id: int):
    db = SessionLocal()
    try:
        payment = db.query(Payment).filter(Payment.id == payment_id).first()

        if not payment:
            logger.error(f"Payment {payment_id} not found in background task")
            return

        logger.info(f"Payment {payment_id} started background processing")
        time.sleep(10)

        payment.status = "completed"
        db.commit()
        db.refresh(payment)

        logger.info(f"Payment {payment_id} completed successfully")

    except Exception as e:
        logger.exception(f"Error while processing payment {payment_id}: {str(e)}")
    finally:
        db.close()


@router.post("/")
def create_claim(
    amount: float,
    description: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    claim = Claim(
        user_id=current_user.id,
        description=description,
        amount=amount,
        status="pending"
    )

    db.add(claim)
    db.commit()
    db.refresh(claim)

    logger.info(f"Claim {claim.id} created by user {current_user.id}")

    return claim


@router.get("/")
def get_my_claims(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    claims = (
        db.query(Claim)
        .filter(Claim.user_id == current_user.id)
        .order_by(Claim.id.desc())
        .all()
    )
    return claims


@router.get("/all")
def get_all_claims(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    claims = db.query(Claim).order_by(Claim.id.desc()).all()
    logger.info(f"Admin user {admin_user.id} fetched all claims")
    return claims


@router.post("/{claim_id}/approve")
def approve_claim(
    claim_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    if claim.status != "pending":
        raise HTTPException(status_code=400, detail="Already processed")

    claim.status = "approved"

    payment = Payment(
        claim_id=claim.id,
        amount=claim.amount,
        status="processing"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    logger.info(
        f"Admin user {admin_user.id} approved claim {claim.id}. "
        f"Payment {payment.id} created with status=processing"
    )

    background_tasks.add_task(process_payment, payment.id)

    return {
        "message": "Payment started (async)",
        "payment_id": payment.id
    }


@router.post("/{claim_id}/reject")
def reject_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    if claim.status != "pending":
        raise HTTPException(status_code=400, detail="Already processed")

    claim.status = "rejected"
    db.commit()
    db.refresh(claim)

    logger.info(f"Admin user {admin_user.id} rejected claim {claim.id}")

    return {
        "message": "Claim rejected",
        "claim_id": claim.id
    }