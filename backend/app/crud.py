import logging
from sqlalchemy.orm import Session
from app.models import User, InterestedClient, Task, Client, GroupLesson,PersonalTraining, PastClient,GymStaff
from app.schemas import InterestedClientCreate, TaskCreate, ClientCreate,GymStaffCreate
from datetime import datetime, date

logger = logging.getLogger(__name__)

def get_user_by_username(db: Session, username: str):
    logger.info(f"Fetching user by username: {username}")
    user = db.query(User).filter(User.username == username).first()
    logger.info(f"Result for username '{username}': {user}")
    return user

def create_user(db: Session, username: str, password: str):
    logger.info(f"Creating new user: username={username}")
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User created: {new_user}")
    return new_user

def get_all_clients(db: Session):
    return db.query(Client).all()

def create_interested_client(db: Session, client: InterestedClientCreate):
    logger.info(f"Creating new interested client: {client}")
    new_client = InterestedClient(**client.dict())
    db.add(new_client)
    db.commit()
    logger.info(f"Interested client created: {new_client}")
    return new_client

def create_task(db: Session, task: TaskCreate):
    logger.info(f"Creating new task: {task}")
    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()
    logger.info(f"Task created: {new_task}")
    return new_task

def get_all_tasks(db: Session):
    logger.info("Fetching all tasks")
    tasks = db.query(Task).all()
    logger.info(f"Fetched tasks: {tasks}")
    return tasks

def delete_task_by_phone_number(db: Session, phone_number: str):
    logger.info(f"Attempting to delete task with phone_number: {phone_number}")
    task = db.query(Task).filter(Task.phone_number == phone_number).first()
    if task:
        db.delete(task)
        db.commit()
        logger.info(f"Task with phone_number {phone_number} deleted successfully.")
        return True
    logger.warning(f"Task with phone_number {phone_number} not found.")
    return False

def create_client(db: Session, client: ClientCreate):
    logger.info(f"Creating new client: {client}")
    new_client = Client(
        phone_number=client.phone_number,
        id_number=client.id_number,
        first_name=client.first_name,
        last_name=client.last_name,
        membership_type=client.membership_type,
        payment_method=client.payment_method,
        date_of_birth=client.date_of_birth
    )
    db.add(new_client)
    db.commit()
    logger.info(f"Client created: {new_client}")
    return new_client

def get_client_by_phone_number(db: Session, phone_number: str):
    return db.query(Client).filter(Client.phone_number == phone_number).first()

def get_client_by_id_number(db: Session, id_number: str):
    return db.query(Client).filter(Client.id_number == id_number).first()

def move_client_to_past(db: Session, phone_number: str, id_number: str):
    """
    Move a client from the 'clients' table to the 'past_clients' table based on phone number and ID number.
    """
    # Find the client by phone number and ID number
    client = db.query(Client).filter(
        Client.phone_number == phone_number,
        Client.id_number == id_number
    ).first()
    if not client:
        return None  # Client not found

    # Create a new PastClient entry
    past_client = PastClient(
        phone_number=client.phone_number,
        id_number=client.id_number,
        first_name=client.first_name,
        last_name=client.last_name,
        date_of_birth=client.date_of_birth,
        membership_type=client.membership_type,
        payment_method=client.payment_method
    )

    # Add to PastClients and remove from Clients
    db.add(past_client)
    db.delete(client)
    db.commit()

    return past_client

def get_all_past_clients(db: Session):
    """
    Fetch all past clients from the database.
    """
    return db.query(PastClient).all()
def add_group_lesson(db: Session, day: str, time: str, class_name: str, instructor_name: str):
    """
    Add a group lesson to the 'group_lessons' table based on day and time
    """
    group_lesson = GroupLesson(
        day=day,
        time=time,
        class_name=class_name,
        instructor_name=instructor_name,
    )
    db.add(group_lesson)  # Add the lesson to the database session
    db.commit()  # Commit the transaction to save changes
    db.refresh(group_lesson)  # Refresh the instance to reflect updated values
    return group_lesson  # Return the newly added lesson

def get_all_group_lessons(db: Session):
    lessons = db.query(GroupLesson).all()
    return [
        {
            "day": lesson.day,
            "time": lesson.time,
            "class_name": lesson.class_name,
            "instructor_name": lesson.instructor_name,
        }
        for lesson in lessons
    ]

def add_personal_training(db: Session, day: str, time: str, trainee_name: str, trainer_name: str):
    """
    Add a personal training session to the table.
    """
    training = PersonalTraining(
        day=day,
        time=time,
        trainee_name=trainee_name,
        trainer_name=trainer_name,
    )
    db.add(training)
    db.commit()
    db.refresh(training)
    return training

def get_weekly_personal_trainings(db: Session):
    """
    Fetch all personal training sessions organized by day.
    """
    trainings = db.query(PersonalTraining).all()
    schedule = {}
    for training in trainings:
        if training.day not in schedule:
            schedule[training.day] = []
        schedule[training.day].append({
            "time": training.time,
            "trainee_name": training.trainee_name,
            "trainer_name": training.trainer_name,
        })
    return schedule

def add_gym_staff(db: Session, first_name: str, last_name: str, role: str, phone_number: str, date_of_birth: date = None):
    """
    Add a new staff member to the gym_staff table.
    """
    staff_member = GymStaff(
        first_name=first_name,
        last_name=last_name,
        role=role,
        phone_number=phone_number,
        date_of_birth=date_of_birth
    )
    db.add(staff_member)
    db.commit()
    db.refresh(staff_member)
    return staff_member

def get_all_gym_staff(db: Session):
    """
    Fetch all staff members from the gym_staff table.
    """
    staff = db.query(GymStaff).all()
    return [
        {
            "id": member.id,  # Include the `id` field
            "first_name": member.first_name,
            "last_name": member.last_name,
            "role": member.role,  # Use role as a string
            "phone_number": member.phone_number,
            "date_of_birth": member.date_of_birth
        }
        for member in staff
    ]

