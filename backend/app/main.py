import logging
from datetime import datetime
from collections import defaultdict
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal,get_db
from app.models import Base, User, InterestedClient, Task, Client,GroupLesson,PersonalTraining,GymStaff
from typing import List, Dict
from app.schemas import InterestedClientCreate, TaskCreate, Task, ClientCreate, Client, GroupLessonCreate,GroupLessonsResponse,GroupLessonSchedule,PersonalTrainingCreate, WeeklyPersonalTrainingsResponse, PersonalTrainingBase,GymStaffCreate, GymStaffResponse, UserCreate, UserResponse
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
from app.crud import create_client, get_client_by_phone_number, get_client_by_id_number, add_group_lesson, get_all_group_lessons,add_personal_training, get_weekly_personal_trainings, move_client_to_past, get_all_past_clients,add_gym_staff, get_all_gym_staff, get_all_clients
from httpx import AsyncClient
from pydantic import BaseModel
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


Base.metadata.create_all(bind=engine)


app = FastAPI()
llm_client = AsyncClient(base_url="http://llm_service:8001")

class LLMChatRequest(BaseModel):
    prompt: str
    context: Optional[str] = None

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

@app.post("/users/", response_model=UserResponse)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Add a new user to the users table
    """
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return create_user(db, username=user.username, password=user.password)

@app.get("/users/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Fetch all users from the users table.
    """
    users = db.query(User).all()
    return users

@app.delete("/users/{username}", status_code=204)
def delete_user(username: str, db: Session = Depends(get_db)):
    """
    Delete a user from the users table by username.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@app.post("/api/llm/chat")
async def forward_to_llm(request: LLMChatRequest):
    """
    Forward chat requests to LLM service
    """
    logger.info(f"Forwarding chat request to LLM service: {request.prompt}")
    try:
        response = await llm_client.post(
            "/chat", 
            json=request.dict()
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error communicating with LLM service: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to process LLM request"
        )

@app.post("/interested_clients/")
def add_interested_client(client: InterestedClientCreate, db: Session = Depends(get_db)):
    """
    Add a new interested client to the 'interested_clients' table and automatically add a task to the 'tasks' table.
    """
    logger.info(f"Adding interested client: {client.first_name} {client.last_name}")

    new_client = create_interested_client(db, client)

    task_description = f"{client.first_name} is interested in a gym membership. Please contact her/him ASAP."
    new_task = TaskCreate(
        first_name=client.first_name,
        last_name=client.last_name,
        phone_number=client.phone_number,
        description=task_description
    )
    create_task(db, new_task)  

    return new_client

@app.get("/clients/", response_model=List[Client])
def read_clients(db: Session = Depends(get_db)):
    return get_all_clients(db)

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
def create_group_lesson(
    group_lesson: GroupLessonCreate,
    db: Session = Depends(get_db)
):
    """
    Add a group lesson to the table based on day and time
    """
    logger.info(f"Adding group lesson: {group_lesson.class_name} with {group_lesson.instructor_name} on {group_lesson.day} at {group_lesson.time}")
    return add_group_lesson(
        db,
        group_lesson.day,
        group_lesson.time,
        group_lesson.class_name,
        group_lesson.instructor_name
    )


@app.get("/group_lessons/", response_model=List[GroupLessonSchedule])
def read_group_lessons(db: Session = Depends(get_db)):
    lessons = db.query(GroupLesson).all()
    return [
        GroupLessonSchedule(
            day=lesson.day,
            lessons=[
                GroupLessonCreate(
                    day=lesson.day,
                    time=lesson.time,
                    class_name=lesson.class_name,
                    instructor_name=lesson.instructor_name
                )
            ]
        ) for lesson in lessons
    ]


@app.get("/group_lessons/schedule/", response_model=GroupLessonsResponse)
def get_schedule(db: Session = Depends(get_db)):
    """
    Fetch the schedule of group lessons, organized by day and sorted by time.
    """
    logger.info("Fetching group lessons schedule")
    lessons = db.query(GroupLesson).all()

    week_order = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

    schedule = defaultdict(list)
    for lesson in lessons:
        schedule[lesson.day].append(
            {
                "day": lesson.day,
                "time": lesson.time,
                "class_name": lesson.class_name,
                "instructor_name": lesson.instructor_name
            }
        )

    for day in schedule:
        schedule[day] = sorted(
            schedule[day],
            key=lambda x: datetime.strptime(x["time"].split("-")[0], "%H:%M")
        )

    ordered_schedule = {day: schedule.get(day, []) for day in week_order}

    return {"schedule": ordered_schedule}

@app.delete("/group_lessons/")
def delete_group_lesson(day: str, time: str, db: Session = Depends(get_db)):
    """
    Delete a group lesson based on day and time.
    """
    logger.info(f"Attempting to delete group lesson: day={day}, time={time}")
    lesson = db.query(GroupLesson).filter(GroupLesson.day == day, GroupLesson.time == time).first()
    if not lesson:
        logger.warning(f"Group lesson not found: day={day}, time={time}")
        raise HTTPException(status_code=404, detail="Group lesson not found")

    db.delete(lesson)
    db.commit()
    logger.info(f"Group lesson deleted successfully: day={day}, time={time}")
    return {"message": "Group lesson deleted successfully"}


@app.post("/personal_trainings/")
def create_personal_training(training: PersonalTrainingCreate, db: Session = Depends(get_db)):
    """
    Add a personal training session.
    """
    logger.info(f"Received personal training data: {training.dict()}") 
    return add_personal_training(
        db=db,
        day=training.day,
        time=training.time,
        trainee_name=training.trainee_name,
        trainer_name=training.trainer_name
    )

@app.get("/personal_trainings/schedule/", response_model=WeeklyPersonalTrainingsResponse)
def get_personal_training_schedule(db: Session = Depends(get_db)):
    """
    Fetch the schedule of personal trainings, organized by day and sorted by time.
    """
    logger.info("Fetching personal training schedule")
    trainings = db.query(PersonalTraining).all()

    week_order = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

    schedule = defaultdict(list)
    for training in trainings:
        schedule[training.day].append(
            {
                "day": training.day,
                "time": training.time,
                "trainee_name": training.trainee_name,
                "trainer_name": training.trainer_name
            }
        )

    for day in schedule:
        schedule[day] = sorted(
            schedule[day],
            key=lambda x: datetime.strptime(x["time"].split("-")[0], "%H:%M")
        )

    ordered_schedule = {day: schedule.get(day, []) for day in week_order}

    return {"schedule": ordered_schedule}

@app.delete("/personal_trainings/", status_code=204)
def delete_personal_training(trainer_name: str, day: str, time: str, db: Session = Depends(get_db)):
    """
    Delete a personal training session by trainer, day, and time.
    """
    logger.info(f"Deleting personal training by {trainer_name} on {day} at {time}")
    training = db.query(PersonalTraining).filter(
        PersonalTraining.trainer_name == trainer_name,
        PersonalTraining.day == day.lower(),
        PersonalTraining.time == time
    ).first()

    if not training:
        logger.warning(f"Personal training by {trainer_name} on {day} at {time} not found.")
        raise HTTPException(status_code=404, detail="Personal training not found")

    db.delete(training)
    db.commit()
    logger.info(f"Personal training by {trainer_name} on {day} at {time} deleted successfully.")
    return {"message": "Personal training deleted successfully"}


@app.post("/clients/move_to_past/")
def move_to_past_client(phone_number: str, id_number: str, db: Session = Depends(get_db)):
    """
    Move a client to the 'Past Clients' table based on phone number and ID number.
    """
    client = move_client_to_past(db, phone_number, id_number)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": f"Client {client.first_name} {client.last_name} moved to past clients successfully."}

@app.get("/past_clients/", response_model=List[Client])
def read_past_clients(db: Session = Depends(get_db)):
    """
    Fetch all past clients from the Past Clients table.
    """
    logger.info("Fetching all past clients")
    past_clients = get_all_past_clients(db)
    return past_clients


@app.post("/gym_staff/", response_model=GymStaffResponse)
def create_gym_staff(staff: GymStaffCreate, db: Session = Depends(get_db)):
    """
    Add a new staff member to the database.
    """
    return add_gym_staff(
        db=db,
        first_name=staff.first_name,
        last_name=staff.last_name,
        role=staff.role,
        phone_number=staff.phone_number,
        date_of_birth=staff.date_of_birth
    )

@app.get("/gym_staff/", response_model=List[GymStaffResponse])
def read_gym_staff(db: Session = Depends(get_db)):
    """
    Fetch all staff members from the database.
    """
    staff = get_all_gym_staff(db)
    return staff

@app.delete("/gym_staff/{staff_id}")
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    """
    Delete a staff member from the gym_staff table.
    """
    staff_member = db.query(GymStaff).filter(GymStaff.id == staff_id).first()
    if not staff_member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    db.delete(staff_member)
    db.commit()
    return {"message": "Staff member deleted successfully"}

@app.on_event("shutdown")
async def shutdown_event():
    await llm_client.aclose()
