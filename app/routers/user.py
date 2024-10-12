from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update, delete
from slugify import slugify

from app.models import User
from app.schemas import CreateUser, UpdateUser
from app.backend.db_depends import get_db


router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get('/user_id')
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalars(select(User).where(User.id == user_id)).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User was not found")


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], user_data: CreateUser):
    existing_user = db.scalars(
        select(User).where((User.username == user_data.username))).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this username already exists.")

    db.execute(insert(User).values(username=user_data.username,
                                   firstname=user_data.firstname,
                                   lastname=user_data.lastname,
                                   age=user_data.age,
                                   slug=slugify(user_data.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,'transaction': 'Successful'}


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, user_update: UpdateUser):
    user = db.execute(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(
        update(User).where(User.id == user_id).values(
            firstname=user_update.firstname,
            lastname=user_update.lastname,
            age=user_update.age))

    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful'}
