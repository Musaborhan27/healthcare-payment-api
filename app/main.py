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

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Healthcare Payment Automation API")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(claim.router)
app.include_router(payment.router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "healthcare-payment-api"
    }


@app.on_event("startup")
def bootstrap_users():
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
            logging.info("Default admin user created successfully")
        else:
            logging.info("Default admin user already exists")

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
            logging.info(f"Demoted {changed_count} accidental admin user(s) to role=user")

    except Exception as e:
        logging.exception(f"Error while bootstrapping users: {str(e)}")
    finally:
        db.close()