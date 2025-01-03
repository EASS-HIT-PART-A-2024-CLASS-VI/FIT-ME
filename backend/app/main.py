from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import Base, User, InterestedClient, Task
from app.schemas import InterestedClientCreate, TaskCreate, Task, CustomerCreate, Customer
from app.crud import (
    get_user_by_username,
    create_user,
    create_interested_client,
    create_task,
    get_all_tasks,
)
from app.crud import (
    get_user_by_username,
    create_user,
    create_interested_client,
    create_task,
    get_all_tasks,
    delete_task_by_phone_number,  # ייבוא הפונקציה החדשה
)
from app.crud import create_customer, get_customer_by_phone_number, get_customer_by_id_number
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to FitMe!"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login/")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"Received login request: {request.username}")
    user = get_user_by_username(db, username=request.username)
    if user and user.password == request.password:
        logger.info(f"Login successful for user: {request.username}")
        return {"message": "Login successful"}
    logger.warning(f"Login failed for user: {request.username}")
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.on_event("startup")
def seed_users():
    logger.info("Seeding initial users...")
    db = SessionLocal()
    try:
        users = [
            {"username": "ordo", "password": "Aa123456"},
            {"username": "Liatsim", "password": "Aa123456"},
            {"username": "sapirha", "password": "Aa123456"},
            {"username": "miriya", "password": "Aa123456"},
            {"username": "viciy", "password": "Aa123456"},
        ]
        for user in users:
            if not get_user_by_username(db, user["username"]):
                create_user(db, username=user["username"], password=user["password"])
                logger.info(f"User created: {user['username']}")
    finally:
        db.close()

@app.post("/interested_clients/")
def add_interested_client(client: InterestedClientCreate, db: Session = Depends(get_db)):
    """
    Add a new interested client to the 'interested_clients' table and automatically add a task to the 'tasks' table.
    """
    logger.info(f"Adding interested client: {client.first_name} {client.last_name}")
    
    # Add interested client to the table
    new_client = create_interested_client(db, client)
    
    # Automatically create a task
    task_description = f"{client.first_name} is interested in a gym membership. Please contact them ASAP."
    new_task = TaskCreate(
        first_name=client.first_name,
        last_name=client.last_name,
        phone_number=client.phone_number,
        description=task_description
    )
    create_task(db, new_task)  # Ensure this line has the correct indentation.

    return new_client

@app.post("/tasks/")
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    logger.info(f"Adding task for client: {task.first_name} {task.last_name}")
    return create_task(db, task)

@app.get("/tasks/", response_model=list[Task])
def get_tasks(db: Session = Depends(get_db)):
    logger.info("Fetching all tasks from the database.")
    tasks = get_all_tasks(db)
    logger.info(f"Total tasks fetched: {len(tasks)}")
    return tasks

@app.delete("/tasks/{phone_number}", status_code=204)
def delete_task(phone_number: str, db: Session = Depends(get_db)):
    logger.info(f"Deleting task with phone_number: {phone_number}")
    task = delete_task_by_phone_number(db, phone_number)
    if not task:
        logger.warning(f"Task with phone_number {phone_number} not found.")
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Task with phone_number {phone_number} deleted successfully.")
    return {"message": "Task deleted successfully"}

@app.post("/customers/", response_model=Customer)
def register_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    logger.info(f"Registering new customer: {customer.first_name} {customer.last_name}")
    existing_customer = get_customer_by_phone_number(db, customer.phone_number)
    if existing_customer:
        raise HTTPException(status_code=400, detail="Customer already exists with this phone number")
    existing_id = get_customer_by_id_number(db, customer.id_number)
    if existing_id:
        raise HTTPException(status_code=400, detail="Customer already exists with this ID number")
    return create_customer(db, customer)

@app.get("/customers/phone/{phone_number}", response_model=Customer)
def get_customer_by_phone(phone_number: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching customer with phone number: {phone_number}")
    customer = get_customer_by_phone_number(db, phone_number)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/customers/id/{id_number}", response_model=Customer)
def get_customer_by_id(id_number: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching customer with ID number: {id_number}")
    customer = get_customer_by_id_number(db, id_number)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
