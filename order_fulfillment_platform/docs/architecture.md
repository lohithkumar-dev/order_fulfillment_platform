# Architecture

```mermaid
flowchart LR
 C[Customer / Admin / Warehouse User] --> API[FastAPI REST API]
 API --> AUTH[JWT + RBAC Dependencies]
 API --> SVC[Service / Domain Layer]
 SVC --> REPO[SQLAlchemy / Repository Queries]
 REPO --> PG[(PostgreSQL)]
 SVC --> N[Notification Service]
 SVC --> A[Audit Service]
 SVC --> I[Inventory Reservation]
 I --> PG
```

Routes validate HTTP input. Services own business rules and transaction boundaries. SQLAlchemy models represent persistent state. PostgreSQL row locks protect inventory reservation and transfers.
