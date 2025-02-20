from typing import List, Dict
from pydantic import BaseModel,Field
from typing import Optional
from datetime import date

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

class ClientBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    id_number: str
    membership_type: str
    payment_method: str
    date_of_birth: date | None = None

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    class Config:
        orm_mode = True

class PastClientBase(BaseModel):
    phone_number: str
    id_number: str
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    membership_type: str
    payment_method: str

    class Config:
        orm_mode = True

class GroupLessonCreate(BaseModel):
    day: str
    time: str
    class_name: str
    instructor_name: str

    class Config:
        orm_mode = True
        from_attributes = True

class GroupLessonsResponse(BaseModel):
    schedule: Dict[str, List[GroupLessonCreate]]

    class Config:
        orm_mode = True
        from_attributes = True

class GroupLessonSchedule(BaseModel):
    day: str
    lessons: List[GroupLessonCreate]

    class Config:
       orm_mode = True 
       from_attributes = True 

class PersonalTrainingBase(BaseModel):
    day: str
    time: str
    trainee_name: str
    trainer_name: str
    class Config:
        orm_mode = True

class PersonalTrainingCreate(PersonalTrainingBase):
    pass

class WeeklyPersonalTrainingsResponse(BaseModel):
    schedule: Dict[str, List[PersonalTrainingBase]]

class GymStaffBase(BaseModel):
    first_name: str
    last_name: str
    role: str
    phone_number: str
    date_of_birth: date

class GymStaffCreate(GymStaffBase):
    pass

class GymStaffResponse(GymStaffBase):
    id: int

    class Config:
        orm_mode = True
