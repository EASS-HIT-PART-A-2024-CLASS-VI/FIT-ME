from typing import List, Dict
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    class Config:
        orm_mode = True

class InterestedClientBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str

class InterestedClientCreate(InterestedClientBase):
    pass

class InterestedClient(InterestedClientBase):
    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    description: str | None = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    class Config:
        orm_mode = True

class MembershipType(str, Enum):
    monthly = "Monthly"
    quarterly = "3-Months"
    yearly = "Yearly"

class PaymentMethod(str, Enum):
    cash = "Cash"
    credit_card = "Credit Card"

class ClientBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    id_number: str
    membership_type: MembershipType
    payment_method: PaymentMethod

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    class Config:
        orm_mode = True

class GroupLessonCreate(BaseModel):
    day: str
    time: str
    class_name: str
    instructor_name: str

class GroupLessonSchedule(BaseModel):
    day: str
    lessons: List[GroupLessonCreate]

class GroupLessonsResponse(BaseModel):
    schedule: Dict[str, List[GroupLessonCreate]]

class PersonalTrainingBase(BaseModel):
    day: str
    time: str
    trainee_name: str
    trainer_name: str

class PersonalTrainingCreate(PersonalTrainingBase):
    pass

class WeeklyPersonalTrainingsResponse(BaseModel):
    schedule: Dict[str, List[PersonalTrainingBase]]
