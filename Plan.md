# 🚀 Backend Developer Intern Assignment Plan
### FastAPI + PostgreSQL + React.js | Full Stack REST API with Auth & RBAC

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Phase-by-Phase Execution Plan](#phase-by-phase-execution-plan)
5. [Database Schema Design](#database-schema-design)
6. [API Design Reference](#api-design-reference)
7. [Security Implementation Checklist](#security-implementation-checklist)
8. [Frontend UI Plan](#frontend-ui-plan)
9. [API Documentation Plan](#api-documentation-plan)
10. [Scalability Note](#scalability-note)
11. [GitHub README Checklist](#github-readme-checklist)
12. [Submission Checklist](#submission-checklist)

---

## 🎯 Project Overview

Build a **Task Management System** with:
- User Registration & Login (JWT Auth)
- Role-Based Access Control (User vs Admin)
- CRUD APIs for **Tasks** (secondary entity)
- API versioning (`/api/v1/`)
- Swagger auto-documentation (built into FastAPI)
- React.js frontend consuming the APIs
- PostgreSQL database

> **Why Tasks?** Simple, relatable, covers all CRUD operations, and demonstrates RBAC naturally (users manage their own tasks; admins manage all tasks).

---

## 🛠️ Tech Stack

| Layer | Technology | Reason |
|---|---|---|
| Backend Framework | FastAPI (Python) | Async, auto-Swagger, fast |
| Database | PostgreSQL | Relational, scalable, industry standard |
| ORM | SQLAlchemy + Alembic | Migrations, Pythonic queries |
| Auth | JWT (python-jose) | Stateless, scalable |
| Password Hashing | bcrypt (passlib) | Industry standard |
| Validation | Pydantic v2 | Built into FastAPI |
| Frontend | React.js + Axios | Component-based, easy API calls |
| API Docs | Swagger UI (auto) + Postman | FastAPI auto-generates Swagger |
| Optional | Redis (caching), Docker | Bonus points |

---

## 📁 Project Structure

```
task-manager-api/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── config.py                # Environment settings (pydantic-settings)
│   │   ├── database.py              # DB session & engine setup
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py        # Main v1 router (includes all sub-routers)
│   │   │       └── endpoints/
│   │   │           ├── auth.py      # /auth/register, /auth/login
│   │   │           ├── users.py     # /users/me, /users/{id} (admin)
│   │   │           └── tasks.py     # CRUD for tasks
│   │   │
│   │   ├── core/
│   │   │   ├── security.py          # JWT create/verify, password hash
│   │   │   └── dependencies.py      # get_current_user, require_admin deps
│   │   │
│   │   ├── models/
│   │   │   ├── user.py              # SQLAlchemy User model
│   │   │   └── task.py              # SQLAlchemy Task model
│   │   │
│   │   └── schemas/
│   │       ├── auth.py              # RegisterRequest, LoginRequest, TokenResponse
│   │       ├── user.py              # UserResponse, UserUpdate
│   │       └── task.py              # TaskCreate, TaskUpdate, TaskResponse
│   │
│   ├── alembic/                     # DB migrations
│   │   ├── env.py
│   │   └── versions/
│   │
│   ├── tests/
│   │   ├── test_auth.py
│   │   └── test_tasks.py
│   │
│   ├── .env                         # Environment variables (gitignored)
│   ├── .env.example                 # Template (committed to git)
│   ├── requirements.txt
│   ├── Dockerfile                   # Optional bonus
│   └── docker-compose.yml           # Optional bonus
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   │   └── axios.js             # Axios instance with JWT interceptor
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── TaskCard.jsx
│   │   │   └── TaskForm.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx        # Protected route
│   │   │   └── AdminPanel.jsx       # Admin-only route
│   │   ├── context/
│   │   │   └── AuthContext.jsx      # Global auth state
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
├── postman/
│   └── TaskManagerAPI.postman_collection.json
│
└── README.md
```

---

## ⏱️ Phase-by-Phase Execution Plan

### ✅ Phase 0: Setup (30 min)

- [ ] Create GitHub repo: `task-manager-api`
- [ ] Set up Python virtual environment
  ```bash
  python -m venv venv
  source venv/bin/activate  # Windows: venv\Scripts\activate
  ```
- [ ] Install dependencies
  ```bash
  pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary \
              python-jose[cryptography] passlib[bcrypt] pydantic-settings \
              python-multipart pytest httpx
  ```
- [ ] Create `requirements.txt`: `pip freeze > requirements.txt`
- [ ] Set up PostgreSQL database locally (or use Supabase free tier)
- [ ] Create `.env` file:
  ```env
  DATABASE_URL=postgresql://user:password@localhost:5432/taskmanager
  SECRET_KEY=your-super-secret-key-change-this-in-production
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=30
  ```
- [ ] Create `.env.example` (same keys, blank values) and commit it
- [ ] Add `.env` to `.gitignore`

---

### ✅ Phase 1: Database Models & Migrations (20 min)

**`app/models/user.py`**
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.database import Base

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

**`app/models/task.py`**
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending)
    priority = Column(Enum(TaskPriority), default=TaskPriority.medium)
    due_date = Column(DateTime(timezone=True), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="tasks")
```

- [ ] Initialize Alembic: `alembic init alembic`
- [ ] Configure `alembic/env.py` to import your models
- [ ] Generate first migration: `alembic revision --autogenerate -m "create users and tasks tables"`
- [ ] Apply migrations: `alembic upgrade head`

---

### ✅ Phase 2: Core Security Module (20 min)

**`app/core/security.py`** — implement these functions:
- `hash_password(password: str) -> str` using `passlib bcrypt`
- `verify_password(plain, hashed) -> bool`
- `create_access_token(data: dict, expires_delta) -> str` using `python-jose`
- `decode_token(token: str) -> dict`

**`app/core/dependencies.py`** — implement FastAPI dependencies:
- `get_db()` — yields DB session
- `get_current_user(token: str, db)` — decodes JWT, fetches user
- `get_current_active_user(user)` — checks `is_active`
- `require_admin(user)` — raises 403 if not admin

---

### ✅ Phase 3: Pydantic Schemas (15 min)

**`app/schemas/auth.py`**
```python
from pydantic import BaseModel, EmailStr, field_validator
import re

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator("username")
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]{3,50}$', v):
            raise ValueError("Username must be 3-50 chars, alphanumeric/underscore only")
        return v

    @field_validator("password")
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    role: str
```

**`app/schemas/task.py`**
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.task import TaskStatus, TaskPriority

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.medium
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime]
    owner_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
```

---

### ✅ Phase 4: API Endpoints (45 min)

#### Auth Endpoints — `app/api/v1/endpoints/auth.py`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login, returns JWT |
| GET | `/api/v1/auth/me` | Get current user info |

**Key implementation notes:**
- On register: check if email/username already exists → return 400 with clear message
- On login: verify password → create JWT → return token + user metadata
- Never return `hashed_password` in any response schema
- Add `refresh_token` endpoint as a bonus

#### Task Endpoints — `app/api/v1/endpoints/tasks.py`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/tasks/` | User | Get own tasks (paginated) |
| POST | `/api/v1/tasks/` | User | Create task |
| GET | `/api/v1/tasks/{id}` | User | Get task by ID (own only) |
| PUT | `/api/v1/tasks/{id}` | User | Update own task |
| DELETE | `/api/v1/tasks/{id}` | User | Delete own task |
| GET | `/api/v1/admin/tasks/` | Admin | Get ALL tasks (paginated) |
| DELETE | `/api/v1/admin/tasks/{id}` | Admin | Delete any task |

**Key implementation notes:**
- Use `skip` and `limit` query params for pagination
- Users can only access their own tasks — filter by `owner_id`
- Return proper HTTP status codes: 201 for create, 404 if not found, 403 for forbidden
- Add query params for filtering: `?status=pending&priority=high`

#### User Endpoints — `app/api/v1/endpoints/users.py`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/users/me` | User | Get own profile |
| PUT | `/api/v1/users/me` | User | Update own profile |
| GET | `/api/v1/admin/users/` | Admin | List all users |
| PUT | `/api/v1/admin/users/{id}/role` | Admin | Change user role |
| DELETE | `/api/v1/admin/users/{id}` | Admin | Deactivate user |

---

### ✅ Phase 5: Main App Setup (15 min)

**`app/main.py`** — configure:
- [ ] CORS middleware (allow `http://localhost:5173` for Vite/React dev)
- [ ] Include v1 router with prefix `/api/v1`
- [ ] Custom exception handlers (return JSON on 404, 422, 500)
- [ ] Add startup event to verify DB connection
- [ ] Global response model with `success`, `data`, `message` envelope (optional but impressive)

**Standard error response format:**
```json
{
  "success": false,
  "message": "Task not found",
  "error_code": "TASK_NOT_FOUND"
}
```

**Standard success response format:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Task created successfully"
}
```

---

### ✅ Phase 6: React.js Frontend (45 min)

- [ ] Create React app: `npm create vite@latest frontend -- --template react`
- [ ] Install dependencies: `npm install axios react-router-dom`

**Pages to build:**

| Page | Route | Access | Features |
|---|---|---|---|
| Login | `/login` | Public | Email + password form, error display |
| Register | `/register` | Public | Full registration form with validation |
| Dashboard | `/dashboard` | Protected | Task list, create/edit/delete tasks |
| Admin Panel | `/admin` | Admin only | All users, all tasks, role management |

**Key frontend implementation:**
- [ ] Create `AuthContext` with `login()`, `logout()`, `user` state
- [ ] Store JWT in `localStorage` (acceptable for internship; note `httpOnly cookie` is more secure)
- [ ] Create Axios instance with request interceptor to attach `Authorization: Bearer <token>`
- [ ] Create response interceptor to handle 401 → auto-logout
- [ ] Create `ProtectedRoute` component that checks auth before rendering
- [ ] Show success/error toast messages from API responses
- [ ] Loading states on all API calls (disable button while loading)

---

### ✅ Phase 7: Testing (20 min)

Write at minimum these test cases using `pytest` + `httpx`:

```
tests/
├── test_auth.py
│   ├── test_register_success
│   ├── test_register_duplicate_email
│   ├── test_login_success
│   ├── test_login_wrong_password
│   └── test_get_me_unauthorized
│
└── test_tasks.py
    ├── test_create_task
    ├── test_get_tasks
    ├── test_update_task
    ├── test_delete_task
    └── test_user_cannot_access_others_task
```

Run with: `pytest tests/ -v`

---

### ✅ Phase 8: Documentation & Postman Collection (15 min)

- [ ] FastAPI Swagger auto-available at `http://localhost:8000/docs`
- [ ] FastAPI ReDoc auto-available at `http://localhost:8000/redoc`
- [ ] Add `tags`, `summary`, `description`, `response_model` to all endpoints
- [ ] Export Postman collection:
  - Create collection with environment variables: `{{base_url}}`, `{{token}}`
  - Add pre-request script to auto-set token after login
  - Organize into folders: Auth, Tasks, Admin

---

### ✅ Phase 9 (Bonus): Docker & Redis (30 min)

**`docker-compose.yml`:**
```yaml
version: "3.9"
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: taskmanager
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports: ["5432:5432"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  backend:
    build: ./backend
    ports: ["8000:8000"]
    depends_on: [db, redis]
    env_file: ./backend/.env

  frontend:
    build: ./frontend
    ports: ["5173:5173"]
    depends_on: [backend]
```

**Redis use cases to implement:**
- Cache user profile lookups (5 min TTL)
- Rate limiting on login endpoint (5 attempts per minute)

---

## 🗄️ Database Schema Design

```
┌─────────────────────────┐         ┌──────────────────────────────┐
│          users          │         │            tasks             │
├─────────────────────────┤         ├──────────────────────────────┤
│ id          INT PK      │◄────────│ id            INT PK         │
│ email       VARCHAR UQ  │  1   *  │ owner_id      INT FK → users │
│ username    VARCHAR UQ  │         │ title         VARCHAR(200)   │
│ hashed_pwd  VARCHAR     │         │ description   VARCHAR(1000)  │
│ role        ENUM        │         │ status        ENUM           │
│ is_active   BOOLEAN     │         │ priority      ENUM           │
│ created_at  TIMESTAMP   │         │ due_date      TIMESTAMP      │
│ updated_at  TIMESTAMP   │         │ created_at    TIMESTAMP      │
└─────────────────────────┘         │ updated_at    TIMESTAMP      │
                                    └──────────────────────────────┘

ENUMS:
  UserRole:      user | admin
  TaskStatus:    pending | in_progress | completed
  TaskPriority:  low | medium | high

INDEXES:
  users:  email (unique), username (unique)
  tasks:  owner_id (FK index), status (query filter), created_at (sort)
```

---

## 🔐 Security Implementation Checklist

- [ ] **Password hashing**: bcrypt with salt rounds ≥ 12 (passlib default)
- [ ] **JWT**: Short expiry (30 min), sign with `HS256`, secret from env
- [ ] **Input validation**: Pydantic models on all request bodies
- [ ] **SQL injection prevention**: SQLAlchemy ORM (parameterized queries)
- [ ] **CORS**: Whitelist only frontend origin, not `*` in production
- [ ] **No sensitive data in responses**: `hashed_password` never in schema
- [ ] **Rate limiting**: On login endpoint (use `slowapi` library or Redis)
- [ ] **Environment variables**: No secrets hardcoded, use `.env` + `pydantic-settings`
- [ ] **HTTPS**: Note in README that production must use HTTPS (nginx/Caddy)
- [ ] **Role check**: Every admin endpoint uses `Depends(require_admin)`

---

## 🖥️ Frontend UI Plan

### Login Page
- Email + Password inputs
- Show/hide password toggle
- "Don't have an account? Register" link
- Display API error messages (invalid credentials, etc.)
- Redirect to dashboard on success

### Register Page
- Username, Email, Password, Confirm Password
- Client-side validation before API call
- Show password strength indicator (bonus)
- Display API error messages (duplicate email, etc.)

### Dashboard (Protected)
- Navbar: username, role badge, logout button
- **Task List**: cards with title, status badge, priority badge, due date
- **Filter bar**: filter by status, priority
- **Create Task** button → modal form
- **Edit** button on each task card → modal with pre-filled form
- **Delete** button with confirmation dialog
- **Pagination**: previous/next buttons

### Admin Panel (Admin only)
- Tab 1: All Users — table with email, role, status, "Change Role" button
- Tab 2: All Tasks — table with owner info, all tasks across users

---

## 📖 API Documentation Plan

### Swagger (auto-generated by FastAPI)
Enhance every endpoint with:
```python
@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=201,
    summary="Create a new task",
    description="Creates a task owned by the currently authenticated user.",
    tags=["Tasks"],
    responses={
        201: {"description": "Task created"},
        401: {"description": "Not authenticated"},
        422: {"description": "Validation error"},
    }
)
```

### Postman Collection Structure
```
📁 Task Manager API
├── 📁 Auth
│   ├── Register User
│   ├── Login (saves token to env var)
│   └── Get Current User
├── 📁 Tasks
│   ├── Get My Tasks
│   ├── Create Task
│   ├── Get Task by ID
│   ├── Update Task
│   └── Delete Task
└── 📁 Admin
    ├── Get All Users
    ├── Change User Role
    ├── Get All Tasks
    └── Delete Any Task
```

---

## 📈 Scalability Note

Include this section in your README:

### Current Architecture
Single-server FastAPI app with PostgreSQL — suitable for early-stage with hundreds of concurrent users.

### Scaling Path

**Horizontal Scaling:**
- FastAPI is stateless (JWT-based auth) → can run multiple instances behind a load balancer (e.g., Nginx, AWS ALB)
- Use connection pooling (PgBouncer) to handle many DB connections from multiple app instances

**Caching Layer:**
- Redis to cache frequently read data (user profiles, task lists) → reduces DB load by 60-80% for read-heavy operations

**Database Scaling:**
- Read replicas for `GET` queries; primary handles writes
- Partition `tasks` table by `owner_id` or date range at high volume

**Microservices Evolution:**
- Auth service → dedicated JWT issuer
- Task service → owns task CRUD
- Notification service → async (Celery + Redis) for due date reminders
- API Gateway (e.g., Kong) handles routing + rate limiting

**Async & Queuing:**
- FastAPI supports `async` natively — use `asyncpg` for async DB calls
- Background tasks (email, webhooks) via Celery + Redis queue

**Deployment:**
- Docker + Kubernetes for container orchestration
- CI/CD pipeline (GitHub Actions) for automated testing & deployment

---

## 📝 GitHub README Checklist

Your `README.md` must include:
- [ ] Project description & features list
- [ ] Tech stack with badges (use shields.io)
- [ ] Architecture diagram (even a simple ASCII one)
- [ ] **Prerequisites** (Python 3.11+, PostgreSQL, Node.js)
- [ ] **Setup instructions** (clone → create env → install → migrate → run)
- [ ] **Environment variables table** (all keys + descriptions)
- [ ] API base URL and versioning note
- [ ] Link to live Swagger docs
- [ ] How to run tests: `pytest tests/ -v`
- [ ] Scalability note section
- [ ] License (MIT)

---

## ✅ Final Submission Checklist

### Backend
- [ ] User registration API with password hashing
- [ ] Login API returns JWT token
- [ ] Protected routes require valid JWT
- [ ] Admin-only routes reject non-admins with 403
- [ ] Task CRUD — all 5 operations working
- [ ] API versioning at `/api/v1/`
- [ ] Input validation via Pydantic (returns 422 on invalid data)
- [ ] Custom error responses (JSON, not HTML)
- [ ] Database migrations via Alembic
- [ ] At least 5 tests passing

### Frontend
- [ ] Register form sends to API and handles errors
- [ ] Login form stores JWT in localStorage
- [ ] Dashboard only loads when authenticated
- [ ] Tasks displayed, can create/edit/delete
- [ ] Success/error messages shown for all actions
- [ ] Admin panel visible only to admin role

### Documentation
- [ ] Swagger UI working at `/docs`
- [ ] Postman collection exported to `postman/` folder
- [ ] README with full setup guide

### Bonus (High Impact)
- [ ] Docker + docker-compose (gets you ahead of 90% of candidates)
- [ ] Redis caching on GET /tasks
- [ ] Rate limiting on /auth/login
- [ ] Refresh token endpoint
- [ ] Soft delete (is_deleted flag instead of hard delete)
- [ ] Task due date email reminders (Celery + SMTP)

---

## ⏰ Suggested Time Budget (within 2 days)

| Phase | Task | Time |
|---|---|---|
| 0 | Setup & project scaffold | 30 min |
| 1 | DB models + migrations | 20 min |
| 2 | Security core (JWT, hashing) | 20 min |
| 3 | Pydantic schemas | 15 min |
| 4 | All API endpoints | 45 min |
| 5 | Main app config & error handling | 15 min |
| 6 | React frontend | 45 min |
| 7 | Tests | 20 min |
| 8 | Postman + README | 20 min |
| 9 | Docker (bonus) | 30 min |
| — | Buffer/debugging | 30 min |
| **Total** | | **~4 hours** |

---

*Good luck! Focus on clean code, proper error handling, and a well-written README — these are what evaluators notice most.*