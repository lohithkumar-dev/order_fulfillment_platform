
from fastapi import FastAPI

from app.core.config import settings
from app.core.exceptions import DomainError, domain_exception_handler
from app.api.v1 import (
    auth,
    products,
    warehouses,
    inventory,
    orders,
    returns,
    dashboard,
)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

# Register custom exception handler
app.add_exception_handler(
    DomainError,
    domain_exception_handler,
)

# Register API routers
routers = [
    auth.router,
    products.router,
    warehouses.router,
    inventory.router,
    orders.router,
    returns.router,
    dashboard.router,
]

for router in routers:
    app.include_router(router, prefix="/api/v1")


# Health check
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
