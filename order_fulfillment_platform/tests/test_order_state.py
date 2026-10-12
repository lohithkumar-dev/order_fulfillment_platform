import pytest
from app.db.models.order import Order,OrderStatus
from app.services.order import change_status
from app.core.exceptions import DomainError
def test_invalid_transition(db,customer):
    o=Order(order_number='ORD-X',customer_id=customer.id,warehouse_id=1,status=OrderStatus.PENDING);db.add(o);db.commit()
    with pytest.raises(DomainError): change_status(db,o,OrderStatus.SHIPPED,customer.id)
