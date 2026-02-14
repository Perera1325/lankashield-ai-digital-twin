from sqlalchemy import Column, Integer, Float, Boolean, DateTime
from database import Base
import datetime


class AnomalyLog(Base):
    __tablename__ = "anomaly_logs"

    id = Column(Integer, primary_key=True, index=True)
    voltage = Column(Float)
    load_percentage = Column(Float)
    temperature = Column(Float)
    anomaly_detected = Column(Boolean)
    risk_score = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
