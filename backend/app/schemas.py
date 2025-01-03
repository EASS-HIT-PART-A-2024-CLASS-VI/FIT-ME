from pydantic import BaseModel
from typing import Optional

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

# Task Schema
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

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    id_number: str
    subscription_type: Optional[str] = "Monthly"
    payment_method: Optional[str] = "Cash"

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    class Config:
        orm_mode = True
