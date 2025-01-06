import logging
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import Base, User, InterestedClient, Task, Client,GroupLesson,PersonalTraining
from app.schemas import InterestedClientCreate, TaskCreate, Task, ClientCreate, Client, GroupLessonCreate,GroupLessonsResponse,GroupLessonSchedule,PersonalTrainingCreate, WeeklyPersonalTrainingsResponse, PersonalTrainingBase
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
    delete_task_by_phone_number,  
)
from app.crud import create_client, get_client_by_phone_number, get_client_by_id_number, add_group_lesson, get_all_group_lessons,add_personal_training, get_weekly_personal_trainings

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
    create_task(db, new_task)  

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

@app.post("/clients/", response_model=Client)
def register_client(client: ClientCreate, db: Session = Depends(get_db)):
    logger.info(f"Registering new client: {client.first_name} {client.last_name}")
    existing_client = get_client_by_phone_number(db, client.phone_number)
    if existing_client:
        raise HTTPException(status_code=400, detail="Client with this phone number already exists")
    existing_id = get_client_by_id_number(db, client.id_number)
    if existing_id:
        raise HTTPException(status_code=400, detail="Client with this ID number already exists")
    return create_client(db, client)

@app.get("/clients/phone/{phone_number}", response_model=Client)
def get_client_by_phone(phone_number: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching client with phone number: {phone_number}")
    client = get_client_by_phone_number(db, phone_number)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.get("/clients/id/{id_number}", response_model=Client)
def get_client_by_id(id_number: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching client with ID number: {id_number}")
    client = get_client_by_id_number(db, id_number)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.post("/group_lessons/")
def create_group_lesson(day: str, time: str, class_name: str, instructor_name: str, db: Session = Depends(get_db)):
    """
    Add a group lesson to the table based on day and time
    """
    logger.info(f"Adding group lesson: {class_name} with {instructor_name} on {day} at {time}")
    return add_group_lesson(db, day, time, class_name, instructor_name)


@app.get("/group_lessons/", response_model=list[GroupLessonCreate])
def read_group_lessons(db: Session = Depends(get_db)):
    """
    Fetch all group lessons from the database.
    """
    logger.info("Fetching all group lessons")
    lessons = get_all_group_lessons(db)
    return [GroupLessonSchema.from_orm(lesson) for lesson in lessons]

@app.get("/group_lessons/schedule/", response_model=GroupLessonsResponse)
def get_schedule(db: Session = Depends(get_db)):
    """
    Fetch the schedule of group lessons, organized by day
    """
    logger.info("Fetching group lessons schedule")
    lessons = db.query(GroupLesson).all()  # Use the GroupLesson from models

    # Organize lessons by day
    schedule = {}
    for lesson in lessons:
        if lesson.day not in schedule:
            schedule[lesson.day] = []
        schedule[lesson.day].append(
            GroupLessonCreate(
                day=lesson.day,
                time=lesson.time,
                class_name=lesson.class_name,
                instructor_name=lesson.instructor_name
            )
        )
    return {"schedule": schedule}

@app.post("/personal_trainings/")
def create_personal_training(
    day: str,
    time: str,
    trainee_name: str,
    trainer_name: str,
    db: Session = Depends(get_db)
):
    """
    Add a personal training session.
    """
    logger.info(f"Adding personal training: {trainee_name} with {trainer_name} on {day} at {time}")
    return add_personal_training(db, day, time, trainee_name, trainer_name)

@app.get("/personal_trainings/schedule/", response_model=WeeklyPersonalTrainingsResponse)
def get_personal_training_schedule(db: Session = Depends(get_db)):
    """
    Fetch the schedule of personal trainings, organized by day
    """
    logger.info("Fetching personal training schedule")
    trainings = db.query(PersonalTraining).all()  # Pull data from the DB

    # Organize trainings by day
    schedule = {}
    for training in trainings:
        if training.day not in schedule:
            schedule[training.day] = []
        schedule[training.day].append(
            PersonalTrainingBase(
                day=training.day,
                time=training.time,
                trainee_name=training.trainee_name,
                trainer_name=training.trainer_name
            )
        )
    return {"schedule": schedule}
