from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from sklearn.ensemble import IsolationForest

app = FastAPI(title="LankaShield AI Engine")

# Train basic anomaly model (prototype)
# Normally trained with historical data
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

    return {
        "anomaly_detected": anomaly,
        "risk_score": round(risk_score, 2),
        "analysis_model": "IsolationForest_v1"
    }
