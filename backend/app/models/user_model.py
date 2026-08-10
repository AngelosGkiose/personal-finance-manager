from sqlalchemy import Column, Integer, String, DateTime

from backend.app.database.database import Base


class UserModel(Base):
    __tablename__ = 'users'
    id =Column(Integer, primary_key=True,index=True)
    username =Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    hashed_password =Column(String,nullable=False)
    created_at=Column(DateTime,nullable=False)
    
