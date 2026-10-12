import pytest
from app.db.models.inventory import Inventory
from app.services.inventory import adjust
from app.core.exceptions import DomainError
def test_inventory_cannot_go_negative(db,customer):
    i=Inventory(warehouse_id=1,product_id=1,quantity=2,reserved_quantity=0,reorder_threshold=1);db.add(i);db.commit()
    with pytest.raises(DomainError): adjust(db,1,1,-3,'bad',customer.id)
