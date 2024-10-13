from app.backend.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    priority = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'),
                     nullable=False, index=True)
    content = Column(String)
    title = Column(String)
    completed = Column(Boolean, default=False)
    slug = Column(String, unique=True, index=True)

    user = relationship('User', back_populates='tasks')
