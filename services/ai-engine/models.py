from sqlalchemy import Column, Integer, Float, Boolean, DateTime, String
from sqlalchemy.sql import func
from database import Base


class AnomalyLog(Base):
    __tablename__ = "anomaly_logs"

    id = Column(Integer, primary_key=True, index=True)
    voltage = Column(Float)
    load_percentage = Column(Float)
    temperature = Column(Float)
    anomaly_detected = Column(Boolean)
    risk_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
