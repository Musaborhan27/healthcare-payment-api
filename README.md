````md
# Healthcare Payment Automation API

A portfolio backend project built with **FastAPI**, **PostgreSQL**, **Redis**, and **Celery** to simulate a healthcare claims and payment workflow with **JWT authentication**, **role-based access control**, and **asynchronous payment processing**.

## Overview

This project models a simplified healthcare reimbursement system.

- Users can register and log in
- Authenticated users can create and view their own claims
- Admins can view all users, review all claims, and approve or reject claims
- Approved claims trigger an asynchronous payment process through Celery
- Payment records are stored in PostgreSQL and can be queried through protected endpoints

This project was built to demonstrate backend engineering skills around:

- REST API design
- authentication and authorization
- async background processing
- service orchestration with Docker Compose
- relational database integration
- role-based business workflows

---

## Tech Stack

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Redis**
- **Celery**
- **JWT Authentication**
- **Docker / Docker Compose**

---

## Architecture

The system is split into four services:

- **api** -> FastAPI application
- **db** -> PostgreSQL database
- **redis** -> message broker / result backend
- **worker** -> Celery worker for async payment processing

### Workflow

1. A user registers and logs in
2. The user creates a claim
3. An admin reviews the claim
4. If approved, the API creates a payment record
5. Celery processes the payment asynchronously
6. The payment status is updated to `completed`

---

## Features

### Authentication and Authorization
- User registration
- JWT-based login
- Protected routes with bearer token
- Role-based access control (`user` and `admin`)

### Claims
- Create claim
- View own claims
- Admin can view all claims
- Admin can approve or reject claims

### Payments
- Async payment processing using Celery
- View own payments
- Admin can view all payments

### Health and Service Readiness
- `/health` endpoint
- Docker Compose health checks for PostgreSQL and Redis
- API startup waits for the database before booting

---

## Project Structure

```bash
.
├── app
│   ├── core
│   │   ├── celery_app.py
│   │   └── security.py
│   ├── db
│   │   └── database.py
│   ├── models
│   │   ├── claim.py
│   │   ├── payment.py
│   │   └── user.py
│   ├── routes
│   │   ├── auth.py
│   │   ├── claim.py
│   │   ├── payment.py
│   │   └── user.py
│   ├── schemas
│   │   └── user.py
│   └── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
````

---

## API Endpoints

### Auth

* `POST /auth/login` -> Login and receive JWT token

### Users

* `POST /users/register` -> Register a new user
* `GET /users/me` -> Get current authenticated user
* `GET /users/` -> Admin only, list all users

### Claims

* `POST /claims/` -> Create claim
* `GET /claims/` -> Get current user claims
* `GET /claims/all` -> Admin only, get all claims
* `POST /claims/{claim_id}/approve` -> Admin only, approve claim
* `POST /claims/{claim_id}/reject` -> Admin only, reject claim

### Payments

* `GET /payments/` -> Get current user payments
* `GET /payments/all` -> Admin only, get all payments

### Health

* `GET /health` -> Health check

---

## Running Locally with Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/Musaborhan27/healthcare-payment-api.git
cd healthcare-payment-api
```

### 2. Start the services

```bash
docker compose up --build
```

This starts:

* FastAPI app on port `8000`
* PostgreSQL on port `5432`
* Redis on port `6379`
* Celery worker in the background

### 3. Open Swagger UI

```bash
http://localhost:8000/docs
```

---

## Environment Notes

The API service uses Docker Compose environment values such as:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/healthcare_db
REDIS_URL=redis://redis:6379/0
```

When running outside Docker, local values typically look like:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/healthcare_db
REDIS_URL=redis://localhost:6379/0
```

---

## Default Admin Bootstrap

On application startup, the system bootstraps a default admin user using values defined in `app/core/security.py`.

That admin account can be used to:

* list all users
* list all claims
* approve claims
* reject claims
* list all payments

---

## Example Tested Flow

The following workflow has been manually verified through Swagger UI:

1. Register a normal user
2. Log in and receive bearer token
3. Access `/users/me`
4. Confirm normal user cannot access admin-only endpoints
5. Create a claim
6. Log in as admin
7. Access `/claims/all`
8. Approve a claim
9. Confirm payment is created asynchronously
10. Confirm `/payments/all` returns a completed payment record

Example result after approval:

```json
[
  {
    "id": 1,
    "claim_id": 1,
    "amount": 1000,
    "status": "completed"
  }
]
```

---

## Data Persistence

PostgreSQL data is stored using a named Docker volume:

```yaml
volumes:
  postgres_data:
```

This means data persists across normal container restarts such as:

```bash
docker compose down
docker compose up -d
```

Do **not** use `docker compose down -v` if you want to preserve data, because `-v` removes the database volume.

---

## Current Status

### Completed

* JWT authentication
* RBAC authorization
* claim creation flow
* admin review flow
* async payment execution with Celery
* Docker Compose setup
* PostgreSQL integration
* Redis integration
* health checks and startup readiness

### Not Yet Added

* automated test suite
* CI/CD pipeline
* production deployment
* API rate limiting
* audit logging
* database migrations with Alembic

---

## Why This Project Matters

This project demonstrates more than CRUD.

It shows how to design a backend workflow where:

* permissions matter
* multiple services coordinate
* async work is separated from request/response cycles
* infrastructure and application startup order matter
* persistent state is stored correctly across container restarts

---

## Next Improvements

* Add automated tests with `pytest`
* Add GitHub Actions CI
* Add Alembic migrations
* Deploy a live demo with Render or Railway
* Add stronger validation and error handling
* Add observability and logging improvements

---

## Author

**Musab Orhan**

Backend portfolio project focused on FastAPI, authentication, RBAC, async workflows, Dockerized services, and production-style backend design.