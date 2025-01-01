from sqlalchemy import Column, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    # שם משתמש
    username = Column(String, primary_key=True, index=True)

    # סיסמה
    password = Column(String, nullable=False)
