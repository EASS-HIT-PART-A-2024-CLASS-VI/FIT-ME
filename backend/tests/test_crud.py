import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.models import Base, User, Client, Task, GroupLesson, PersonalTraining, GymStaff
from app.schemas import ClientCreate, TaskCreate
from app.crud import (
    create_user, get_user_by_username,
    create_client, get_client_by_phone_number, 
    create_task, get_all_tasks, delete_task_by_phone_number,
    add_group_lesson, get_all_group_lessons,
    add_personal_training, get_weekly_personal_trainings,
    add_gym_staff, get_all_gym_staff
)

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(db):
    user = create_user(db, "testuser", "password123")
    assert user.username == "testuser"

def test_get_user_by_username(db):
    create_user(db, "testuser2", "password456")
    user = get_user_by_username(db, "testuser2")
    assert user is not None
    assert user.username == "testuser2"

def test_create_client(db):
    client_data = ClientCreate(
        phone_number="123456789",
        id_number="987654321",
        first_name="John",
        last_name="Doe",
        membership_type="Premium",
        payment_method="Credit Card",
        date_of_birth="1990-01-01"
    )
    client = create_client(db, client_data)
    assert client.phone_number == "123456789"

def test_get_client_by_phone_number(db):
    client_data = ClientCreate(
        phone_number="123456789",
        id_number="987654321",
        first_name="John",
        last_name="Doe",
        membership_type="Premium",
        payment_method="Credit Card",
        date_of_birth="1990-01-01"
    )
    create_client(db, client_data)
    client = get_client_by_phone_number(db, "123456789")
    assert client is not None

def test_create_task(db):
    task_data = TaskCreate(
        phone_number="111222333",
        first_name="John",
        last_name="Doe",
        description="Follow-up call"
    )
    task = create_task(db, task_data)
    assert task.phone_number == "111222333"

def test_get_all_tasks(db):
    create_task(db, TaskCreate(
        phone_number="555555555",
        first_name="Jane",
        last_name="Smith",
        description="New client follow-up"
    ))
    tasks = get_all_tasks(db)
    assert len(tasks) > 0

def test_delete_task_by_phone_number(db):
    create_task(db, TaskCreate(
        phone_number="555555555",
        first_name="Lisa",
        last_name="Brown",
        description="Meeting"
    ))
    result = delete_task_by_phone_number(db, "555555555")
    assert result is True

def test_add_group_lesson(db):
    lesson = add_group_lesson(db, "Monday", "10:00", "Yoga", "Alice")
    assert lesson.class_name == "Yoga"

def test_get_all_group_lessons(db):
    add_group_lesson(db, "Monday", "10:00", "Yoga", "Alice")
    lessons = get_all_group_lessons(db)
    assert len(lessons) > 0

def test_add_personal_training(db):
    training = add_personal_training(db, "Tuesday", "15:00", "Bob", "Coach Mike")
    assert training.trainer_name == "Coach Mike"

def test_get_weekly_personal_trainings(db):
    add_personal_training(db, "Tuesday", "15:00", "Bob", "Coach Mike")
    schedule = get_weekly_personal_trainings(db)
    assert "Tuesday" in schedule

def test_add_gym_staff(db):
    staff = add_gym_staff(
        db,
        first_name="Lisa",
        last_name="Smith",
        role="Trainer",
        phone_number="999999999",
        date_of_birth=datetime.strptime("1995-07-21", "%Y-%m-%d").date()
    )
    assert staff.role == "Trainer"

def test_get_all_gym_staff(db):
    add_gym_staff(
        db,
        first_name="Mike",
        last_name="Johnson",
        role="Manager",
        phone_number="888888888",
        date_of_birth=datetime.strptime("1985-06-15", "%Y-%m-%d").date()
    )
    staff = get_all_gym_staff(db)
    assert len(staff) > 0

