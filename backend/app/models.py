from sqlalchemy import Column, String, Integer,Date, Enum, PrimaryKeyConstraint, Time, ForeignKey, Date
from app.database import Base
from sqlalchemy.orm import relationship

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
    membership_type = Column(String, nullable=False)
    payment_method = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)

    __table_args__ = (PrimaryKeyConstraint('phone_number', 'id_number', name='client_pk'),) # phone_number and id_number as primary key

class PastClient(Base):
    __tablename__ = "past_clients"

    phone_number = Column(String, nullable=False)
    id_number = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    membership_type = Column(String, nullable=False)
    payment_method = Column(String, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('phone_number', 'id_number', name="past_clients_pk"),  # Composite primary key
    )


class GroupLesson(Base):
    __tablename__ = "group_lessons"

    day = Column(String, nullable=False)  #The format for example - Sunday
    time = Column(String, nullable=False)  #The format for example - 08:00-08:55
    class_name = Column(String, nullable=False)
    instructor_name = Column(String, nullable=False)

    #day and time together as primary key
    __table_args__ = (
        PrimaryKeyConstraint('day', 'time'),
    )

class PersonalTraining(Base):
    __tablename__ = "personal_trainings"

    day = Column(String, nullable=False)
    time = Column(String, nullable=False)
    trainee_name = Column(String, nullable=False)
    trainer_name = Column(String, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('trainer_name', 'day', 'time', name='personal_training_pk'),
    )

class GymStaff(Base):
    __tablename__ = "gym_staff"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    date_of_birth = Column(Date, nullable=False)
