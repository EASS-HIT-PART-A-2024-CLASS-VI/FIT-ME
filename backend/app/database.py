from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL של ה-Database (התאם לערכים שהוגדרו ב-docker-compose.yml)
SQLALCHEMY_DATABASE_URL = "postgresql://gym_admin:GymPass123@db:5432/manage_gym_db"

# יצירת Engine שיתחבר ל-Database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal משמש ליצירת סשנים לעבודה מול ה-Database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# הגדרת בסיס עבור המודלים (ORM)
Base = declarative_base()

