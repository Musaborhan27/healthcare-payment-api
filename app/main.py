import logging
import time

from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
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

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(claim.router)
app.include_router(payment.router)


def wait_for_db(max_attempts: int = 30, delay_seconds: int = 2) -> None:
    for attempt in range(1, max_attempts + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info("Database connection established")
            return
        except OperationalError as exc:
            logger.warning(
                "Database not ready yet (attempt %s/%s): %s",
                attempt,
                max_attempts,
                exc,
            )
            time.sleep(delay_seconds)

    raise RuntimeError("Database did not become ready in time")


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
        else:
            logger.info("Default admin user already exists")

        accidental_admins = (
            db.query(User)
            .filter(User.email != ADMIN_EMAIL, User.role == "admin")
            .all()
        )

        changed_count = 0
        for user_record in accidental_admins:
            user_record.role = "user"
            changed_count += 1

        if changed_count > 0:
            db.commit()
            logger.info(
                "Demoted %s accidental admin user(s) to role=user",
                changed_count
            )

    except Exception:
        db.rollback()
        logger.exception("Error while bootstrapping users")
        raise
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    wait_for_db()
    Base.metadata.create_all(bind=engine)
    bootstrap_users()


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "healthcare-payment-api"
    }