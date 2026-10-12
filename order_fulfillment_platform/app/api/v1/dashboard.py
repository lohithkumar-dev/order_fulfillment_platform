from fastapi import APIRouter,Depends
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.order import Order,OrderStatus
from app.db.models.inventory import Inventory
from app.dependencies.auth import current_user
router=APIRouter(prefix='/dashboard',tags=['Dashboard'])
@router.get('/summary')
def summary(db:Session=Depends(get_db),user=Depends(current_user)):
    if user.role.value=='customer':
        return {'orders':db.scalar(select(func.count()).select_from(Order).where(Order.customer_id==user.id)) or 0,'delivered':db.scalar(select(func.count()).select_from(Order).where(Order.customer_id==user.id,Order.status==OrderStatus.DELIVERED)) or 0}
    return {'orders':db.scalar(select(func.count()).select_from(Order)) or 0,'pending':db.scalar(select(func.count()).select_from(Order).where(Order.status==OrderStatus.PENDING)) or 0,'low_stock':db.scalar(select(func.count()).select_from(Inventory).where((Inventory.quantity-Inventory.reserved_quantity)<=Inventory.reorder_threshold)) or 0}
