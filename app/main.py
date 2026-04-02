import logging

from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.core.security import ADMIN_EMAIL, ADMIN_PASSWORD, get_password_hash
from app.db.database import Base, SessionLocal, engine
from app.models.user import User
from app.routes import auth, claim, payment, user

import app.models.claim
import app.models.payment
import app.models.user

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Healthcare Payment Automation API")

# ROUTES
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(claim.router)
app.include_router(payment.router)


# ROOT ENDPOINT
@app.get("/")
def root():
    return {"message": "API is running"}


# HEALTH CHECK
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "healthcare-payment-api"
    }


def bootstrap_users() -> None:
    db: Session = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.email == ADMIN_EMAIL).first()

        if not admin_user:
            admin_user = User(
                email=ADMIN_EMAIL,
                password=get_password_hash(ADMIN_PASSWORD),
                role="admin",
                refresh_token=None,
            )
            db.add(admin_user)
            db.commit()
            logger.info("Default admin user created successfully")

    except Exception:
        db.rollback()
        logger.exception("Error while bootstrapping users")
        raise
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    bootstrap_users()