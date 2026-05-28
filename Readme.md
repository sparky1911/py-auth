# Auth Service

A production-oriented authentication service built using FastAPI, PostgreSQL, Docker, and JWT authentication.

## Tech Stack

* Python 3.12
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT Authentication
* Docker
* Docker Compose
* Makefile
* AWS EC2 (planned)
* AWS RDS (planned)
* GitHub Actions CI/CD (planned)

---

# Features

* User Signup
* User Login
* JWT Access Tokens
* Password Hashing using Argon2
* PostgreSQL Integration
* Dockerized Development Environment
* Environment Separation (Dev / Prod)
* Docker Compose Setup
* Health Check Endpoint

---

# Project Structure

```text
auth-service/
│
├── app/
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── schemas.py
│
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── Dockerfile
├── Makefile
├── requirements.txt
├── .gitignore
├── .dockerignore
├── .env.dev
└── .env.prod
```

---

# Local Development Setup

## Clone Repository

```bash
git clone <YOUR_REPO_URL>
cd auth-service
```

---

# Environment Variables

Create `.env.dev`

```env
DATABASE_URL=postgresql://postgres:password@db:5432/authdb

SECRET_KEY=mydevsecret

ALGORITHM=HS256
```

---

# Run Development Environment

Start services:

```bash
make dev
```

Stop services:

```bash
make dev-down
```

View logs:

```bash
make dev-logs
```

---

# Access API

Swagger UI:

```text
http://localhost:8000/docs
```

Health Endpoint:

```text
http://localhost:8000/health
```

---

# API Endpoints

## Signup

### POST `/signup`

Request:

```json
{
  "email": "test@test.com",
  "username": "testuser",
  "password": "password123"
}
```

---

## Login

### POST `/login`

Request:

```json
{
  "email": "test@test.com",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "<JWT_TOKEN>"
}
```

---

# Docker Commands

Build image manually:

```bash
docker build -t auth-service .
```

Run container manually:

```bash
docker run -p 8000:8000 auth-service
```

---

# Makefile Commands

| Command          | Description                    |
| ---------------- | ------------------------------ |
| `make dev`       | Start development environment  |
| `make dev-down`  | Stop development environment   |
| `make dev-logs`  | View development logs          |
| `make prod`      | Start production environment   |
| `make prod-down` | Stop production environment    |
| `make clean`     | Remove unused Docker resources |

---

# Development Architecture

```text
FastAPI Container
        ↓
PostgreSQL Container
```

Using Docker Compose networking.

---

# Production Architecture

```text
AWS EC2
    ↓
FastAPI Docker Container
    ↓
AWS RDS PostgreSQL
```

---

# Upcoming Improvements

* Refresh Tokens
* RBAC (Role-Based Access Control)
* Alembic Migrations
* Redis Integration
* Nginx Reverse Proxy
* HTTPS
* GitHub Actions CI/CD
* Structured Logging
* Rate Limiting

---

# Security Notes

* Passwords are hashed using Argon2
* Environment variables are excluded from Git
* JWT authentication is stateless
* Database credentials are externalized

---

# Author

Backend authentication service project for backend engineering and cloud deployment practice.
