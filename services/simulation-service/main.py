from fastapi import FastAPI
import random
import datetime
from typing import List

app = FastAPI(title="LankaShield Simulation Service")

# In-memory storage (temporary for prototype)
grid_history = []
ev_history = []
telecom_history = []


def generate_grid_node():
    data = {
        "node_id": f"GRID_{random.randint(1,10)}",
        "voltage": round(random.uniform(210, 250), 2),
        "load_percentage": round(random.uniform(40, 100), 2),
        "temperature": round(random.uniform(30, 80), 2),
        "timestamp": datetime.datetime.utcnow()
    }
    grid_history.append(data)
    return data


def generate_ev_station():
    data = {
        "station_id": f"EV_{random.randint(1,5)}",
        "charging_power_kw": round(random.uniform(5, 50), 2),
        "active_sessions": random.randint(1, 10),
        "timestamp": datetime.datetime.utcnow()
    }
    ev_history.append(data)
    return data


def generate_telecom_tower():
    data = {
        "tower_id": f"TOWER_{random.randint(1,3)}",
        "network_traffic_mbps": round(random.uniform(100, 1000), 2),
        "packet_loss_percentage": round(random.uniform(0, 5), 2),
        "timestamp": datetime.datetime.utcnow()
    }
    telecom_history.append(data)
    return data


# --- Generate New Data Endpoints ---

import requests

AI_ENGINE_URL = "http://127.0.0.1:8001/analyze"

@app.get("/simulate/grid")
def simulate_grid():
    grid_data = generate_grid_node()

    try:
        response = requests.post(
            AI_ENGINE_URL,
            json={
                "voltage": grid_data["voltage"],
                "load_percentage": grid_data["load_percentage"],
                "temperature": grid_data["temperature"]
            },
            timeout=5
        )
        ai_result = response.json()
    except Exception as e:
        ai_result = {"error": str(e)}

    return {
        "grid_data": grid_data,
        "ai_analysis": ai_result
    }


@app.get("/simulate/ev")
def simulate_ev():
    return generate_ev_station()


@app.get("/simulate/telecom")
def simulate_telecom():
    return generate_telecom_tower()


# --- Historical Data Endpoints ---

@app.get("/history/grid", response_model=List[dict])
def get_grid_history():
    return grid_history


@app.get("/history/ev", response_model=List[dict])
def get_ev_history():
    return ev_history


@app.get("/history/telecom", response_model=List[dict])
def get_telecom_history():
    return telecom_history
