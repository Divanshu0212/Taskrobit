# Task Manager API + Frontend

A full-stack internship assignment project with robust FastAPI backend, PostgreSQL, JWT auth, RBAC, Redis-enhanced bonuses, and a React frontend.

## Features

- JWT authentication with register, login, refresh, and me endpoints
- Role-based access control with admin-only routes
- Task CRUD with filters, pagination, and ownership checks
- Redis login rate limiting and cache helpers
- Alembic migration setup
- Automated tests with pytest
- React frontend with protected routes and admin panel
- Docker Compose for full local stack

## Stack

- Backend: FastAPI, SQLAlchemy, Alembic, PostgreSQL, Redis
- Frontend: React, Vite, React Router, Axios
- Security: bcrypt password hashing, JWT tokens

## Local Setup

### 1) Backend

- Go to backend folder
- Create virtual environment and install dependencies
- Create .env from .env.example
- Run migrations
- Start server

Commands:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# fill .env values
alembic upgrade head
uvicorn app.main:app --reload
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3) Docker Full Stack

```bash
docker compose up --build
```

## API Docs

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Admin Portal Access

Admin UI route:

- http://localhost:5173/admin

How to get an admin account:

1. Register a normal account from UI (`/register`) or API.
2. Promote that account to admin.

Using Docker:

```bash
cd /home/divanshu/Desktop/Intern
docker-compose exec backend python scripts/promote_to_admin.py --email your_email@example.com
```

Using local backend (non-Docker):

```bash
cd /home/divanshu/Desktop/Intern/backend
python scripts/promote_to_admin.py --email your_email@example.com
```

After promotion:

1. Login again on http://localhost:5173/login.
2. Open http://localhost:5173/admin.

## Roles and Permissions

### user

- Can register, login, refresh token, and view own profile.
- Can create, view, update, and delete only own tasks.
- Cannot access admin endpoints or admin panel.

### admin

- Has all `user` permissions.
- Can view all users.
- Can change any user's role.
- Can deactivate users.
- Can view and delete any task in the system.
- Can access admin UI at `/admin`.

## Tests

```bash
cd backend
pytest tests -v
```

## Environment Variables

| Key | Description |
|---|---|
| DATABASE_URL | PostgreSQL SQLAlchemy URL |
| SECRET_KEY | JWT signing secret |
| ALGORITHM | JWT algorithm (HS256) |
| ACCESS_TOKEN_EXPIRE_MINUTES | Access token expiry |
| REDIS_URL | Redis connection URL |
| RATE_LIMIT_LOGIN_ATTEMPTS | Max login attempts in window |
| RATE_LIMIT_WINDOW_SECONDS | Rate limit window size |
| CACHE_TTL_SECONDS | Cache TTL in seconds |
| CORS_ORIGINS | CSV allowed CORS origins |

## Scalability Note

Current architecture supports early-stage usage with a single FastAPI instance.
Scaling path:

- Horizontal scaling with load balancer because JWT auth is stateless
- Redis caching for read-heavy endpoints
- PostgreSQL read replicas for heavy read traffic
- Async workers for reminders and notifications (Celery + Redis)
- Container orchestration with Kubernetes and CI/CD pipeline

## License

MIT
