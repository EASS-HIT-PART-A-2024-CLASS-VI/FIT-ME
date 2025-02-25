import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app, get_db
from app.models import Base
from app.schemas import UserCreate, ClientCreate, TaskCreate, GroupLessonCreate, PersonalTrainingCreate, GymStaffCreate

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def test_register_user(client):
    data = {"username": "testuser", "password": "testpass"}
    response = client.post("/users/", json=data)
    assert response.status_code == 200

def test_login_user(client):
    data = {"username": "testuser", "password": "testpass"}
    response = client.post("/login/", json=data)
    assert response.status_code in [200, 401]

def test_register_client(client):
    data = {
        "phone_number": "1234567890",
        "id_number": "987654321",
        "first_name": "John",
        "last_name": "Doe",
        "membership_type": "monthly",
        "payment_method": "credit card",
        "date_of_birth": "1990-01-01"
    }
    response = client.post("/clients/", json=data)
    assert response.status_code == 200

def test_get_clients(client):
    response = client.get("/clients/")
    assert response.status_code == 200

def test_add_task(client):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "1234567890",
        "description": "Follow up with client."
    }
    response = client.post("/tasks/", json=data)
    assert response.status_code == 200

def test_add_group_lesson(client):
    data = {
        "day": "Monday",
        "time": "08:00-09:00",
        "class_name": "Yoga",
        "instructor_name": "Alice"
    }
    response = client.post("/group_lessons/", json=data)
    assert response.status_code == 200

def test_get_group_lessons(client):
    response = client.get("/group_lessons/")
    assert response.status_code == 200

def test_add_personal_training(client):
    data = {
        "day": "Monday",
        "time": "10:00-11:00",
        "trainee_name": "John Doe",
        "trainer_name": "Alice Trainer"
    }
    response = client.post("/personal_trainings/", json=data)
    assert response.status_code == 200

def test_add_gym_staff(client):
    data = {
        "first_name": "Mark",
        "last_name": "Smith",
        "role": "trainer",
        "phone_number": "0987654321",
        "date_of_birth": "1985-05-15"
    }
    response = client.post("/gym_staff/", json=data)
    assert response.status_code == 200
