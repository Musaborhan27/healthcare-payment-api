````md
# Healthcare Payment Automation API

A backend portfolio project built with FastAPI that simulates a healthcare claims and payment workflow with JWT authentication, role-based access control, and asynchronous payment processing.

## Overview

This project models a simplified healthcare reimbursement system.

Users can create insurance claims, while admins review and approve or reject them. Once a claim is approved, the system creates a payment record and processes it asynchronously.

The goal of this project is to demonstrate backend engineering fundamentals beyond basic CRUD, including authentication, authorization, workflow logic, async processing, and container-ready project structure.

## Features

- JWT-based authentication
- Role-Based Access Control (RBAC)
- User and admin flows
- Claim creation and review workflow
- Asynchronous payment state transition
- Seeded default admin account
- Health check endpoint
- Swagger UI documentation
- Docker support

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- JWT
- Passlib / bcrypt
- FastAPI BackgroundTasks
- Docker

## Important Note

The current async workflow uses `FastAPI BackgroundTasks` to simulate asynchronous processing.

This is suitable for demonstrating backend workflow design, but it is not a distributed job queue. A more production-oriented next step would be replacing this with Celery + Redis or another real queue system.

## Roles

### User
A normal user can:

- register
- log in
- view their profile
- create claims
- view only their own claims
- view only their own payments

A normal user cannot:

- approve claims
- reject claims
- view all claims
- view all payments

### Admin
An admin can:

- log in
- view all users
- view all claims
- approve claims
- reject claims
- view all payments

## Default Admin Account

The application seeds an admin user automatically at startup.

- **Email:** `admin@healthcare.local`
- **Password:** `admin123`

## API Endpoints

### Auth
- `POST /auth/login`

### Users
- `POST /users/register`
- `GET /users/me`
- `GET /users/`

### Claims
- `POST /claims/`
- `GET /claims/`
- `GET /claims/all`
- `POST /claims/{claim_id}/approve`
- `POST /claims/{claim_id}/reject`

### Payments
- `GET /payments/`
- `GET /payments/all`

### Health
- `GET /health`

## Example Workflow

### User Flow
1. Register a user
2. Log in as that user
3. Authorize in Swagger with the bearer token
4. Create a claim
5. View own claims
6. Attempt to approve claim
7. Receive `403 Admin access required`

### Admin Flow
1. Log in as admin
2. Authorize in Swagger with the admin bearer token
3. View all claims
4. Approve a pending claim
5. View all payments
6. Observe payment state transition from `processing` to `completed`

## Verified Behavior

This project has been tested for the following behaviors:

- user login works successfully
- `GET /users/me` returns the correct user role
- normal users can create claims
- normal users cannot approve claims
- admins can view all claims
- admins can approve claims
- approved claims create payment records
- payments complete asynchronously after approval

## Payment Processing Logic

When an admin approves a claim:

1. the claim status changes from `pending` to `approved`
2. a payment record is created with status `processing`
3. a background task starts
4. after a short delay, the payment status changes to `completed`

This simulates an async backend workflow commonly found in real systems.

## Health Check

The API includes a simple health endpoint:

```bash
GET /health
````

Example response:

```json
{
  "status": "ok",
  "service": "healthcare-payment-api"
}
```

## Local Setup

Clone the project and run it locally:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Swagger UI

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

## Docker

### Build the image

```bash
docker build -t healthcare-payment-api .
```

### Run the container

```bash
docker run -p 8000:8000 healthcare-payment-api
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Project Structure

```bash
app/
├── core/
│   └── security.py
├── db/
│   └── database.py
├── models/
│   ├── user.py
│   ├── claim.py
│   └── payment.py
├── routes/
│   ├── auth.py
│   ├── user.py
│   ├── claim.py
│   └── payment.py
├── schemas/
└── main.py

Dockerfile
README.md
requirements.txt
.gitignore
.dockerignore
```

## What This Project Demonstrates

This project demonstrates the ability to build:

* authenticated backend APIs
* role-based access control
* workflow-driven business logic
* asynchronous state transitions
* admin/user separation
* container-ready backend services

## Limitations

This project intentionally keeps some parts simple:

* uses SQLite instead of PostgreSQL
* uses BackgroundTasks instead of a real queue
* does not yet include automated tests
* does not yet include rate limiting
* does not yet include CI/CD

These are reasonable next improvements, not hidden weaknesses.

## Next Improvements

Planned upgrades for a more production-oriented version:

* PostgreSQL integration
* Celery + Redis for real background jobs
* pytest test suite
* rate limiting
* better error handling
* structured logging
* monitoring / observability
* environment-based configuration
* CI/CD pipeline
