from sqlalchemy import Column, String, Integer, Enum, PrimaryKeyConstraint
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

class Customer(Base):
    __tablename__ = "customers"

    phone_number = Column(String, nullable=False)
    id_number = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    subscription_type = Column(Enum("Monthly", "Yearly", "3 Months", name="subscription_types"), default="Monthly")
    payment_method = Column(Enum("Cash", "Credit Card", name="payment_methods"), default="Cash")

    __table_args__ = (
        PrimaryKeyConstraint('phone_number', 'id_number'),
    )
