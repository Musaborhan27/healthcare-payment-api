# Healthcare Payment Automation API

A backend system built with **FastAPI** for managing healthcare claims, payments, and user authentication.

This project demonstrates:

* RESTful API design
* Authentication with JWT
* Database integration with SQLAlchemy
* Automated testing with Pytest

---

## Tech Stack

* **FastAPI**
* **SQLAlchemy**
* **SQLite (local & test)**
* **PostgreSQL (production-ready)**
* **Pytest**
* **JWT Authentication**

---

## Installation

```bash
git clone https://github.com/Musaborhan27/healthcare-payment-api.git
cd healthcare-payment-api

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## Run the Application

```bash
uvicorn app.main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Run Tests

```bash
pytest
```

---

## Authentication

The API uses JWT-based authentication.

Default admin user is created automatically on startup:

```
email: admin@example.com
password: admin
```

---

## Database

* Uses **SQLite** for local development and testing
* Supports **PostgreSQL** via `DATABASE_URL`

Example:

```env
DATABASE_URL=sqlite:///./test.db
```

---

## Project Structure

```
app/
├── core/        # security, config
├── db/          # database setup
├── models/      # SQLAlchemy models
├── routes/      # API endpoints
├── schemas/     # Pydantic schemas
└── main.py      # app entrypoint

tests/           # test cases
```

---

## Features

* User registration & login
* JWT authentication
* Claims management
* Payment processing
* Role-based access (admin/user)
* Automated tests

---

## Future Improvements

* Docker support
* CI/CD pipeline
* API rate limiting
* Logging & monitoring improvements

---

## License

This project is for educational purposes.
