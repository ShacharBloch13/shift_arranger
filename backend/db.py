from sqlalchemy import create_engine, Column, Integer, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from datetime import datetime

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/ShiftArranger"

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the assignments table
class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    assignments = Column(JSON, nullable=False)
    grade = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

# Initialize the database
Base.metadata.create_all(bind=engine)


def get_saturday_night_worker(db: Session):
    if db.query(Assignment).count() == 0:
        return None

    last_assignment = db.query(Assignment).order_by(Assignment.date.desc()).first()
    if last_assignment:
        assignments = last_assignment.assignments
        name = assignments.get("Saturday 23:00-07:00") # This is taking very long, maybe we should change
        return name
    return None