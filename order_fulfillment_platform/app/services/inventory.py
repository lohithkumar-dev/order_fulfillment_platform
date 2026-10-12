from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.inventory import Inventory, InventoryTransaction, InventoryTransactionType
from app.db.models.product import Product
from app.core.exceptions import DomainError

def get_locked(db:Session, warehouse_id:int, product_id:int):
    inv=db.execute(select(Inventory).where(Inventory.warehouse_id==warehouse_id, Inventory.product_id==product_id).with_for_update()).scalar_one_or_none()
    if not inv: raise DomainError('INVENTORY_NOT_FOUND','Inventory record not found',404)
    return inv

def reserve(db:Session, warehouse_id:int, product_id:int, qty:int, user_id:int, reference_id:str):
    inv=get_locked(db,warehouse_id,product_id)
    available=inv.quantity-inv.reserved_quantity
    if available < qty: raise DomainError('INSUFFICIENT_INVENTORY',f'Only {available} units available',409)
    inv.reserved_quantity += qty
    db.add(InventoryTransaction(product_id=product_id,warehouse_id=warehouse_id,transaction_type=InventoryTransactionType.RESERVATION,quantity=qty,user_id=user_id,reference_entity='order',reference_id=reference_id,metadata_json={'available_after':available-qty}))

def release(db:Session, warehouse_id:int, product_id:int, qty:int, user_id:int, reference_id:str):
    inv=get_locked(db,warehouse_id,product_id)
    if inv.reserved_quantity < qty: raise DomainError('INVALID_RELEASE','Reserved quantity is insufficient',409)
    inv.reserved_quantity -= qty
    db.add(InventoryTransaction(product_id=product_id,warehouse_id=warehouse_id,transaction_type=InventoryTransactionType.RELEASE,quantity=qty,user_id=user_id,reference_entity='order',reference_id=reference_id))

def adjust(db:Session, warehouse_id:int, product_id:int, amount:int, reason:str, user_id:int):
    inv=get_locked(db,warehouse_id,product_id); previous=inv.quantity; new=previous+amount
    if new < inv.reserved_quantity or new < 0: raise DomainError('INVALID_ADJUSTMENT','Adjustment would make inventory negative or below reservations',409)
    inv.quantity=new
    db.add(InventoryTransaction(product_id=product_id,warehouse_id=warehouse_id,transaction_type=InventoryTransactionType.ADJUSTMENT,quantity=amount,user_id=user_id,reference_entity='inventory',reference_id=str(inv.id),metadata_json={'previous_quantity':previous,'new_quantity':new,'reason':reason}))
