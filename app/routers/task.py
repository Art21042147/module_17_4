from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update, delete
from slugify import slugify

from app.models import Task, User
from app.schemas import CreateTask, UpdateTask, CreateUser
from app.backend.db_depends import get_db


router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/task_id')
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalars(select(Task).where(Task.id == task_id)).first()
    if task:
        return task
    raise HTTPException(status_code=404, detail="Task was not found")


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)],
                      task_data: CreateTask,
                      user_id: int):
    existing_user = db.scalars(select(User).where(User.id == user_id)).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(insert(Task).values(priority=task_data.priority,
                                   user_id=user_id,
                                   content=task_data.content,
                                   title=task_data.title,
                                   slug=slugify(task_data.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)],
                      task_id: int, task_update: UpdateTask):
    task = db.execute(select(Task).where(Task.id == task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task was not found")

    db.execute(
        update(Task).where(Task.id == task_id).values(
            title=task_update.firstname,
            content=task_update.content,
            priority=task_update.priority))

    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}



@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task was not found")

    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Tasks deleted successfully'}
