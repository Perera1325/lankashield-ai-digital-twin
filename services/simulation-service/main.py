from fastapi import FastAPI
import random
import datetime

app = FastAPI(title="LankaShield Simulation Service")


def generate_grid_node():
    return {
        "node_id": f"GRID_{random.randint(1,10)}",
        "voltage": round(random.uniform(210, 250), 2),
        "load_percentage": round(random.uniform(40, 100), 2),
        "temperature": round(random.uniform(30, 80), 2),
        "timestamp": datetime.datetime.utcnow()
    }


def generate_ev_station():
    return {
        "station_id": f"EV_{random.randint(1,5)}",
        "charging_power_kw": round(random.uniform(5, 50), 2),
        "active_sessions": random.randint(1, 10),
        "timestamp": datetime.datetime.utcnow()
    }


def generate_telecom_tower():
    return {
        "tower_id": f"TOWER_{random.randint(1,3)}",
        "network_traffic_mbps": round(random.uniform(100, 1000), 2),
        "packet_loss_percentage": round(random.uniform(0, 5), 2),
        "timestamp": datetime.datetime.utcnow()
    }


@app.get("/simulate/grid")
def simulate_grid():
    return generate_grid_node()


@app.get("/simulate/ev")
def simulate_ev():
    return generate_ev_station()


@app.get("/simulate/telecom")
def simulate_telecom():
    return generate_telecom_tower()
