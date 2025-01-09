# FIT-ME Project

<img align="right" src="READMEPHOTO.jpg" width="200">

## Overview
The **FIT-ME** application is a comprehensive gym management system designed to streamline gym operations. It includes features for managing client registrations, handling group and personal training schedules, tracking staff roles, and monitoring task assignments to ensure efficient workflows. The system aims to provide a seamless and user-friendly experience for both gym staff and members.

The backend is built using FastAPI and containerized using Docker and communicates with a PostgreSQL database for data management and storage.

In the future, this project will also include a frontend designed to interact seamlessly with the backend.
---

## Table of Contents
1. [Technologies Used](#technologies-used)
2. [Project Features](#project-features)
3. [Project Structure](#project-structure)
4. [Endpoints](#endpoints)
5. [How to Run the Project](#how-to-run-the-project)
6. [Future Work](#future-work)
7. [Contact Info](#contact-info)

---

## Technologies Used

### Backend
- **Python**: 3.10+
- **FastAPI**: A modern, fast web framework for APIs.
- **SQLAlchemy**: Database ORM for managing queries.
- **Pydantic**: For data validation and parsing.
- **psycopg2-binary**: PostgreSQL database adapter.

### Database
- **PostgreSQL**: Version 13 for relational data storage.

### Containerization
- **Docker**: Containerized backend for simplified deployment.
- **Docker Compose**: Manages multi-container services.

---

## Project Features

### Backend
- **User Authentication**: Login functionality for authorized staff.
- **Client Management**:
  - Manage potential and current clients.
  - Automatic task creation for follow-ups.
  - Move clients to a "Past Clients" archive.
- **Group Lessons**:
  - Schedule group lessons by day and time.
  - Fetch lesson schedules.
- **Personal Training**:
  - Manage and fetch personal training schedules.
- **Gym Staff**: Add and fetch staff details with specific roles.
- **Logging**: System-wide logging for debugging and auditing.

---

## Project Structure

```
manage_gym/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Empty initializer file
│   │   ├── main.py              # FastAPI backend logic and endpoints
│   │   ├── models.py            # Database models
│   │   ├── schemas.py           # Data validation schemas
│   │   ├── crud.py              # Database operations
│   │   ├── database.py          # Database connection setup
│   │   ├── enums.py             # Enums for multiple choice variables
│   ├── Dockerfile               # Backend container configuration
│   ├── requirements.txt         # Backend dependencies
├── docker-compose.yml           # Multi-container orchestration
└── README.md                    # Documentation
```

---

## Endpoints

### User Management
- **POST /login/**
  - Login with username and password.

### Client Management
- **POST /clients/**: Add a new client.
- **GET /clients/phone/{phone_number}**: Fetch client by phone number.
- **POST /clients/move_to_past/**: Move client to past clients.

### Task Management
- **POST /tasks/**: Create a new task.
- **GET /tasks/**: Fetch all tasks.
- **DELETE /tasks/{phone_number}**: Delete a task by phone number.

### Group Lessons
- **POST /group_lessons/**: Add a new group lesson.
- **GET /group_lessons/**: Fetch all group lessons.

### Personal Training
- **POST /personal_trainings/**: Add a personal training session.
- **GET /personal_trainings/schedule/**: Fetch the weekly training schedule.

---

## How to Run the Project

### Prerequisites
- Docker and Docker Compose installed.

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/miri-y/manage_gym.git
   cd manage_gym
   ```
2. **Build and Run Containers**:
   ```bash
   docker-compose up --build
   ```
   - The backend will be available at: `http://localhost:8000`
   - Explore API docs at: `http://localhost:8000/docs`

3. **Access PostgreSQL**:
   ```bash
   docker exec -it manage_gym_postgres psql -U gym_admin -d manage_gym_db
   ```

---

## Future Work
- Add a compatible frontend to interact with the backend.
- Update the backend to meet the requirements of the frontend.
- Create a user-friendly design for the application.
- Improve communication between backend and frontend components.

---

## Contact Info
**Project Author**: Miri Y.  
**Email**:(mailto:miriamyakobson200021@gmail.com)  
**GitHub**: [miri-y](https://github.com/miri-y)

