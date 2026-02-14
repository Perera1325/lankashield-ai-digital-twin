# System Architecture – LankaShield

## 1. Architectural Vision

LankaShield follows a microservices-based distributed architecture designed to simulate, monitor, analyze, and optimize critical infrastructure systems in real time.

The architecture separates concerns into independent services for scalability, maintainability, and resilience.

---

## 2. High-Level Components

The system consists of five core layers:

1. Simulation Layer
2. AI Intelligence Layer
3. API Gateway Layer
4. Monitoring Dashboard Layer
5. Infrastructure & DevOps Layer

---

## 3. Component Breakdown

### 3.1 Simulation Service

Purpose:
- Simulate power grid nodes
- Simulate EV charging stations
- Simulate telecom tower activity
- Generate time-series data

Technology:
- Python
- FastAPI

Output:
- Voltage levels
- Load metrics
- Traffic logs
- Energy consumption

---

### 3.2 AI Intelligence Engine

Purpose:
- Detect anomalies in infrastructure data
- Identify abnormal voltage spikes
- Detect API abuse patterns
- Predict overload risks

Planned Models:
- Isolation Forest
- Z-score detection
- LSTM (advanced stage)

---

### 3.3 API Gateway Layer

Purpose:
- Secure service communication
- Provide authentication (JWT)
- Apply rate limiting
- Log all traffic

Planned Integration:
- WSO2-style API management

---

### 3.4 Monitoring Dashboard

Purpose:
- Visualize infrastructure in real-time
- Display anomaly alerts
- Show load distribution graphs
- Display risk scores

Technology:
- React
- WebSockets
- Chart libraries

---

### 3.5 DevOps Infrastructure

Purpose:
- Containerization (Docker)
- Orchestration (Kubernetes)
- CI/CD pipeline
- Cloud deployment

---

## 4. Data Flow

Simulation Service → AI Engine → API Gateway → Dashboard

If anomaly detected:
AI Engine → Alert System → Dashboard Notification

---

## 5. Scalability Considerations

- Microservices allow independent scaling
- AI engine can be scaled horizontally
- API Gateway can enforce throttling
- Database replication planned for future

---

## 6. Future Enhancements

- Zero Trust Architecture
- Blockchain-based log integrity
- Federated learning across distributed nodes
- Real-world IoT device integration
