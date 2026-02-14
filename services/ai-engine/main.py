from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
from models import AnomalyLog

# Create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LankaShield AI Engine")

# Train basic anomaly model
model = IsolationForest(contamination=0.1)
training_data = np.random.uniform(low=0, high=100, size=(100, 3))
model.fit(training_data)


class InfrastructureData(BaseModel):
    voltage: float
    load_percentage: float
    temperature: float


@app.post("/analyze")
def analyze(data: InfrastructureData):

    input_data = np.array([[data.voltage, data.load_percentage, data.temperature]])
    prediction = model.predict(input_data)

    anomaly = bool(prediction[0] == -1)
    risk_score = float(np.random.uniform(0.5, 1.0)) if anomaly else float(np.random.uniform(0.0, 0.4))

    # Save to database
    db: Session = SessionLocal()
    new_log = AnomalyLog(
        voltage=data.voltage,
        load_percentage=data.load_percentage,
        temperature=data.temperature,
        anomaly_detected=anomaly,
        risk_score=risk_score
    )
    db.add(new_log)
    db.commit()
    db.close()

    return {
        "anomaly_detected": anomaly,
        "risk_score": round(risk_score, 2),
        "analysis_model": "IsolationForest_v1"
    }


@app.get("/logs")
def get_logs():
    db: Session = SessionLocal()
    logs = db.query(AnomalyLog).all()
    db.close()

    return [
        {
            "id": log.id,
            "voltage": log.voltage,
            "load_percentage": log.load_percentage,
            "temperature": log.temperature,
            "anomaly_detected": log.anomaly_detected,
            "risk_score": log.risk_score,
            "created_at": log.created_at
        }
        for log in logs
    ]
