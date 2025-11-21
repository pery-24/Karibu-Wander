from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'wandermatch.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Your existing profile fields
    full_name = Column(String, nullable=True)
    age = Column(Integer, default=25)
    gender = Column(String, default="Rather not say")
    bio = Column(Text, default="")
    travel_style = Column(String, default="")
    instagram = Column(String, default="")

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True)
    creator_name = Column(String)
    destination = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    budget_level = Column(Integer)
    vibe = Column(Text)
    max_people = Column(Integer, default=6)
    current_people = Column(Integer, default=1)
    
    # ← ADD THIS LINE 
    description = Column(Text, nullable=True)   

class JoinRequest(Base):
    __tablename__ = "join_requests"
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer)
    requester_name = Column(String)
    status = Column(String, default="pending")

# THIS LINE WILL AUTOMATICALLY ADD THE MISSING COLUMN
Base.metadata.create_all(bind=engine)