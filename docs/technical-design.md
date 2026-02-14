# Technical Design Document – LankaShield

## 1. System Overview

LankaShield is built as a distributed microservices system where each service has a clearly defined responsibility.

Services communicate via REST APIs and will later support asynchronous messaging.

---

## 2. Microservices Design

### 2.1 Simulation Service

Responsibility:
- Generate synthetic infrastructure data

Endpoints (Planned):

GET /simulate/grid
GET /simulate/ev
GET /simulate/telecom

Data Format Example:

{
  "node_id": "GRID_01",
  "voltage": 231.4,
  "load": 78.2,
  "temperature": 42.5,
  "timestamp": "2026-02-14T10:22:31"
}

---

### 2.2 AI Engine Service

Responsibility:
- Process incoming time-series data
- Detect anomalies
- Calculate risk scores

Endpoints (Planned):

POST /analyze

Input:
Infrastructure JSON data

Output:

{
  "node_id": "GRID_01",
  "anomaly_detected": true,
  "risk_score": 0.87,
  "anomaly_type": "Voltage Spike"
}

---

### 2.3 API Gateway Layer

Responsibility:
- Authentication
- Authorization
- Rate limiting
- Logging

Security Model:
- JWT authentication
- Role-based access control (RBAC)
- Throttling policies

Roles:
- Admin
- Infrastructure Operator
- Viewer

---

### 2.4 Dashboard Service

Responsibility:
- Display real-time metrics
- Show anomaly alerts
- Visualize historical trends

Data Retrieval:
- API polling (initial phase)
- WebSocket streaming (later phase)

---

## 3. Database Design

Planned Database: PostgreSQL

### Tables

1. infrastructure_nodes

- id (Primary Key)
- node_type (grid / ev / telecom)
- location
- status

2. infrastructure_metrics

- id (Primary Key)
- node_id (Foreign Key)
- voltage
- load
- temperature
- timestamp

3. anomaly_logs

- id (Primary Key)
- node_id
- anomaly_type
- risk_score
- detected_at

---

## 4. Communication Strategy

Phase 1:
- REST-based synchronous communication

Phase 2:
- Kafka or message queue for event streaming

---

## 5. Security Architecture

- API Gateway authentication
- Encrypted communication (HTTPS)
- Audit logging
- Rate limiting
- Input validation

---

## 6. Scalability Plan

- AI service horizontally scalable
- Stateless services
- Containerized deployment
- Database indexing for performance

---

## 7. Deployment Strategy

- Docker containerization
- Docker Compose for local testing
- Kubernetes for production
- CI/CD via GitHub Actions
