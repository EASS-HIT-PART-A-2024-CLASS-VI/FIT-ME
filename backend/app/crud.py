import logging
from sqlalchemy.orm import Session
from app.models import User, InterestedClient, Task, Customer
from app.schemas import InterestedClientCreate, TaskCreate, CustomerCreate

logger = logging.getLogger(__name__)

def get_user_by_username(db: Session, username: str):
    logger.info(f"Fetching user by username: {username}")
    user = db.query(User).filter(User.username == username).first()
    logger.info(f"Result for username '{username}': {user}")
    return user

def create_user(db: Session, username: str, password: str):
    logger.info(f"Creating new user: username={username}")
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User created: {new_user}")
    return new_user

def create_interested_client(db: Session, client: InterestedClientCreate):
    logger.info(f"Creating new interested client: {client}")
    new_client = InterestedClient(**client.dict())
    db.add(new_client)
    db.commit()
    logger.info(f"Interested client created: {new_client}")
    return new_client

def create_task(db: Session, task: TaskCreate):
    logger.info(f"Creating new task: {task}")
    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()
    logger.info(f"Task created: {new_task}")
    return new_task

def get_all_tasks(db: Session):
    logger.info("Fetching all tasks")
    tasks = db.query(Task).all()
    logger.info(f"Fetched tasks: {tasks}")
    return tasks

def delete_task_by_phone_number(db: Session, phone_number: str):
    logger.info(f"Attempting to delete task with phone_number: {phone_number}")
    task = db.query(Task).filter(Task.phone_number == phone_number).first()
    if task:
        db.delete(task)
        db.commit()
        logger.info(f"Task with phone_number {phone_number} deleted successfully.")
        return True
    logger.warning(f"Task with phone_number {phone_number} not found.")
    return False

def create_customer(db: Session, customer: CustomerCreate):
    new_customer = Customer(**customer.dict())
    db.add(new_customer)
    db.commit()
    return new_customer

def get_customer_by_phone_number(db: Session, phone_number: str):
    return db.query(Customer).filter(Customer.phone_number == phone_number).first()

def get_customer_by_id_number(db: Session, id_number: str):
    return db.query(Customer).filter(Customer.id_number == id_number).first()
