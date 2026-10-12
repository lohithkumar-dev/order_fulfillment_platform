# Order Fulfillment & Inventory Management Platform

Production-oriented FastAPI backend assignment covering authentication, RBAC, warehouse authorization, product/catalog management, inventory, reservations, orders, fulfillment, returns, notifications, audit logging, idempotency, PostgreSQL transactions, and automated tests.

## Stack
- Python 3.12
- FastAPI + Pydantic v2
- PostgreSQL 16
- SQLAlchemy 2.x
- Alembic
- Pytest
- Docker Compose

## Run locally
```bash
cp .env.example .env
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```
Swagger: `http://localhost:8000/docs`

## Docker
```bash
cp .env.example .env
docker compose up --build
```

## Concurrency strategy
Inventory reservations are performed inside the same database transaction as order creation. The inventory row is selected with PostgreSQL `SELECT ... FOR UPDATE` through SQLAlchemy `with_for_update()`. This serializes competing reservations for the same `(warehouse_id, product_id)` row. Available stock is calculated as `quantity - reserved_quantity`, and a reservation is rejected when insufficient stock remains. The transfer operation locks both inventory rows in deterministic warehouse-ID order to reduce deadlock risk. A unique constraint on `(warehouse_id, product_id)` prevents duplicate inventory records.

## Transaction boundaries
Order creation, reservation records, order items, audit entry and notification are committed together. Cancellation releases reservations and records release transactions in the same unit of work. Warehouse transfers update source/destination quantities and create both immutable transaction records before commit.

## Authorization
- Admin: global management.
- Warehouse Manager: authorized warehouse operations.
- Fulfillment Agent: order processing within authorized warehouse scope.
- Customer: own orders and returns.

For a production submission, add a dependency that checks the current user's `WarehouseAccess` before every warehouse-scoped mutation/read.

## Idempotency
Critical order creation accepts `Idempotency-Key`. The `(user_id, key)` unique constraint makes repeated requests addressable. A production hardening step should additionally lock/create the idempotency row before executing the business operation and store a request fingerprint to reject key reuse with a different payload.

## Order state machine
`PENDING -> CONFIRMED -> ASSIGNED -> PROCESSING -> SHIPPED -> DELIVERED`

Cancellation is permitted before fulfillment reaches the irreversible shipping stage. Invalid transitions return a domain error with HTTP 409.

## Inventory transaction immutability
`inventory_transactions` is append-only by application convention. Normal API routes never expose update/delete operations. In production, database privileges should also deny UPDATE/DELETE to the application role.

## Testing
```bash
pytest -q
```
The test suite includes password/token tests, invalid state transition tests, and negative inventory tests. Expand it with PostgreSQL integration tests for row-lock concurrency, refresh-token rotation/revocation, warehouse authorization, idempotency races, and complete return/fulfillment workflows before final submission.

## API groups
- `/api/v1/auth`
- `/api/v1/products`
- `/api/v1/warehouses`
- `/api/v1/inventory`
- `/api/v1/orders`
- `/api/v1/returns`
- `/api/v1/dashboard`

## Deliverables
The repository includes source code, database models, Alembic configuration, tests, Docker files, Postman collection, ER diagram source, architecture diagram source, and setup documentation.
