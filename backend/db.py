from sqlalchemy import create_engine, Column, Integer, JSON, DateTime, VARCHAR, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func


DATABASE_URL = "mysql+pymysql://root:@localhost:3306/ShiftArranger"

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the assignments table
class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(VARCHAR, primary_key=True)
    assignments = Column(JSON, nullable=False)
    grade = Column(Integer, nullable=False)
    date = Column(DateTime, default=func.now())
    SaturdayNight = Column(VARCHAR, nullable=False)
    manager= Column(VARCHAR, nullable=False)

# Initialize the database
Base.metadata.create_all(bind=engine)


def get_saturday_night_worker(db: Session):
    if db.query(Assignment).count() == 0:
        return None
    return db.query(Assignment).order_by(Assignment.date.desc()).first().SaturdayNight