from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import Base, User
from app.crud import get_user_by_username, create_user
import logging

# הגדרת לוגים
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# יצירת טבלאות ב-DB אם הן לא קיימות
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FitMe!"}

# תלות ב-DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# מודל לנתוני התחברות
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login/")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"Received login request: {request}")
    user = get_user_by_username(db, username=request.username)
    if user and user.password == request.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

# יצירת משתמשים מורשים בעת עליית השרת
@app.on_event("startup")
def seed_users():
    db = SessionLocal()
    try:
        if not get_user_by_username(db, "ordo"):
            create_user(db, username="ordo", password="Aa123456")
        if not get_user_by_username(db, "Liatsim"):
            create_user(db, username="Liatsim", password="Aa123456")
        if not get_user_by_username(db, "sapirha"):
            create_user(db, username="sapirha", password="Aa123456")
        if not get_user_by_username(db, "miriya"):
            create_user(db, username="miriya", password="Aa123456")
        if not get_user_by_username(db, "viciy"):
            create_user(db, username="viciy", password="Aa123456")
    finally:
        db.close()

