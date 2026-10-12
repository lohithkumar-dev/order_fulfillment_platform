from decimal import Decimal
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.product import Product
from app.db.models.order import Order, OrderItem, OrderStatus, OrderStatusHistory
from app.db.models.warehouse import Warehouse
from app.services.inventory import reserve, release
from app.core.exceptions import DomainError

TRANSITIONS={
 OrderStatus.PENDING:{OrderStatus.CONFIRMED,OrderStatus.CANCELLED},
 OrderStatus.CONFIRMED:{OrderStatus.ASSIGNED,OrderStatus.CANCELLED},
 OrderStatus.ASSIGNED:{OrderStatus.PROCESSING,OrderStatus.CANCELLED},
 OrderStatus.PROCESSING:{OrderStatus.SHIPPED},
 OrderStatus.SHIPPED:{OrderStatus.DELIVERED},
 OrderStatus.DELIVERED:set(), OrderStatus.CANCELLED:set()
}

def create_order(db:Session,user_id:int,warehouse_id:int,items):
    wh=db.get(Warehouse,warehouse_id)
    if not wh or not wh.is_active: raise DomainError('WAREHOUSE_UNAVAILABLE','Warehouse is unavailable',400)
    products={p.id:p for p in db.execute(select(Product).where(Product.id.in_([i.product_id for i in items]))).scalars()}
    if len(products)!=len({i.product_id for i in items}): raise DomainError('PRODUCT_NOT_FOUND','One or more products do not exist',404)
    if any(not p.is_active for p in products.values()): raise DomainError('INACTIVE_PRODUCT','Inactive product cannot be ordered',400)
    order=Order(order_number='ORD-'+uuid4().hex[:12].upper(),customer_id=user_id,warehouse_id=warehouse_id,total_amount=0,status=OrderStatus.PENDING)
    db.add(order); db.flush()
    total=Decimal('0')
    for item in items:
        p=products[item.product_id]; line=(p.price*item.quantity)-item.discount+item.tax
        reserve(db,warehouse_id,p.id,item.quantity,user_id,str(order.id))
        db.add(OrderItem(order_id=order.id,product_id=p.id,quantity=item.quantity,unit_price=p.price,discount=item.discount,tax=item.tax,total=line)); total+=line
    order.total_amount=total
    db.add(OrderStatusHistory(order_id=order.id,to_status=order.status.value,user_id=user_id))
    return order

def change_status(db:Session,order:Order,new_status:OrderStatus,user_id:int):
    if new_status not in TRANSITIONS[order.status]: raise DomainError('INVALID_ORDER_TRANSITION',f'Cannot change {order.status.value} to {new_status.value}',409)
    old=order.status; order.status=new_status
    db.add(OrderStatusHistory(order_id=order.id,from_status=old.value,to_status=new_status.value,user_id=user_id))
    if new_status==OrderStatus.CANCELLED:
        for item in db.execute(select(OrderItem).where(OrderItem.order_id==order.id)).scalars(): release(db,order.warehouse_id,item.product_id,item.quantity,user_id,str(order.id))
