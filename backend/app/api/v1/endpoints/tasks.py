from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_admin, require_standard_user
from app.models.task import Task, TaskPriority, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


router = APIRouter()
admin_router = APIRouter()


@router.get("/", response_model=list[TaskResponse], summary="List current user tasks")
def list_my_tasks(
    skip: int = 0,
    limit: int = Query(default=10, le=100),
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    priority_filter: TaskPriority | None = Query(default=None, alias="priority"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_standard_user),
):
    query = db.query(Task).filter(Task.owner_id == current_user.id)
    if status_filter:
        query = query.filter(Task.status == status_filter)
    if priority_filter:
        query = query.filter(Task.priority == priority_filter)
    return query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, summary="Create a task")
def create_task(payload: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(require_standard_user)):
    task = Task(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        due_date=payload.due_date,
        owner_id=current_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskResponse, summary="Get a task by id")
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_standard_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse, summary="Update own task")
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_standard_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete own task")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_standard_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None


@admin_router.get("/", response_model=list[TaskResponse], summary="Admin list all tasks")
def list_all_tasks(
    skip: int = 0,
    limit: int = Query(default=20, le=200),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return db.query(Task).order_by(Task.created_at.desc()).offset(skip).limit(limit).all()


@admin_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Admin delete any task")
def admin_delete_task(task_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None
