from sqlalchemy import Column, String, Integer, Enum, PrimaryKeyConstraint, Time, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship
from app.schemas import MembershipType, PaymentMethod
from app.enums import MembershipType, PaymentMethod,RoleType

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    password = Column(String, nullable=False)

class InterestedClient(Base):
    __tablename__ = "interested_clients"
    phone_number = Column(String, primary_key=True, index=True, nullable=False)  # phone_number as primary key
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)


class Task(Base):
    __tablename__ = "tasks"
    phone_number = Column(String, primary_key=True, index=True, nullable=False)  # phone_number as primary key
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    description = Column(String)

    def __init__(self, first_name, last_name, phone_number, description=None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.description = description or f"{self.first_name} is interested in a gym membership. Please contact them ASAP."

class Client(Base):
    __tablename__ = "clients"

    phone_number = Column(String, nullable=False)
    id_number = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    membership_type = Column(Enum(MembershipType), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)

    __table_args__ = (PrimaryKeyConstraint('phone_number', 'id_number', name='client_pk'),)

class PastClient(Base):
    __tablename__ = "past_clients"

    phone_number = Column(String, nullable=False)
    id_number = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    membership_type = Column(Enum(MembershipType), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)

    __table_args__ = (PrimaryKeyConstraint('phone_number', 'id_number', name="past_clients_pk"),)

class GroupLesson(Base):
    __tablename__ = "group_lessons"

    day = Column(String, nullable=False)  # Day of the lesson (e.g., Sunday)
    time = Column(String, nullable=False)  # Time of the lesson (e.g., 08:00-08:55)
    class_name = Column(String, nullable=False)  # Name of the class
    instructor_name = Column(String, nullable=False)  # Name of the instructor

    # Define a composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('day', 'time'),
    )

class PersonalTraining(Base):
    __tablename__ = "personal_trainings"
    day = Column(String, nullable=False, primary_key=True)  # Day of the week
    time = Column(String, nullable=False, primary_key=True)  # Time of the session
    trainee_name = Column(String, nullable=False)  # Name of the trainee
    trainer_name = Column(String, nullable=False)  # Name of the trainer

class GymStaff(Base):
    __tablename__ = "gym_staff"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)  # First name of the staff member
    last_name = Column(String, nullable=False)  # Last name of the staff member
    role = Column(Enum(RoleType), nullable=False)  # Role from a predefined list (Enum)
    phone_number = Column(String, nullable=False, unique=True)  #Phone number of the staff member
