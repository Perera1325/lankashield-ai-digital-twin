from fastapi import FastAPI, WebSocket, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
import numpy as np
from sklearn.ensemble import IsolationForest
import asyncio

from database import engine, SessionLocal, Base
from models import AnomalyLog, User
from auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    get_db,
)

# --------------------------------------------------
# DATABASE INIT
# --------------------------------------------------
Base.metadata.create_all(bind=engine)

# --------------------------------------------------
# CREATE DEFAULT ADMIN USER
# --------------------------------------------------
db = SessionLocal()
if not db.query(User).filter(User.username == "admin").first():
    new_user = User(
        username="admin",
        hashed_password=get_password_hash("admin123"),
    )
    db.add(new_user)
    db.commit()
db.close()

# --------------------------------------------------
# FASTAPI INIT
# --------------------------------------------------
app = FastAPI(title="LankaShield AI Engine")

# --------------------------------------------------
# CORS
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# AI MODEL
# --------------------------------------------------
model = IsolationForest(contamination=0.2)
training_data = np.random.uniform(0, 100, size=(200, 3))
model.fit(training_data)

# --------------------------------------------------
# WEBSOCKET CONNECTIONS
# --------------------------------------------------
active_connections: List[WebSocket] = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        active_connections.remove(websocket)


async def broadcast(message: dict):
    for connection in active_connections:
        await connection.send_json(message)

# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------
class InfrastructureData(BaseModel):
    voltage: float
    load_percentage: float
    temperature: float

# --------------------------------------------------
# LOGIN ENDPOINT
# --------------------------------------------------
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}

# --------------------------------------------------
# ANALYZE ENDPOINT (PROTECTED)
# --------------------------------------------------
@app.post("/analyze")
async def analyze(
    data: InfrastructureData,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    input_data = np.array([[data.voltage, data.load_percentage, data.temperature]])
    prediction = model.predict(input_data)

    anomaly = bool(prediction[0] == -1)

    risk_score = (
        float(np.random.uniform(0.6, 1.0))
        if anomaly
        else float(np.random.uniform(0.0, 0.4))
    )

    new_log = AnomalyLog(
        voltage=data.voltage,
        load_percentage=data.load_percentage,
        temperature=data.temperature,
        anomaly_detected=anomaly,
        risk_score=risk_score,
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    # Broadcast to dashboard
    asyncio.create_task(
        broadcast(
            {
                "id": new_log.id,
                "voltage": new_log.voltage,
                "load_percentage": new_log.load_percentage,
                "temperature": new_log.temperature,
                "anomaly_detected": new_log.anomaly_detected,
                "risk_score": new_log.risk_score,
                "created_at": str(new_log.created_at),
            }
        )
    )

    return {
        "anomaly_detected": anomaly,
        "risk_score": risk_score,
    }

# --------------------------------------------------
# FETCH LOGS (PROTECTED)
# --------------------------------------------------
@app.get("/logs")
def get_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    logs = db.query(AnomalyLog).order_by(AnomalyLog.id).all()

    return [
        {
            "id": log.id,
            "voltage": log.voltage,
            "load_percentage": log.load_percentage,
            "temperature": log.temperature,
            "anomaly_detected": log.anomaly_detected,
            "risk_score": log.risk_score,
            "created_at": str(log.created_at),
        }
        for log in logs
    ]
