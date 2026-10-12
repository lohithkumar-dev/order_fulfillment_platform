from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.inventory import Inventory
from app.db.models.user import User
from app.schemas.inventory import InventoryCreate,InventoryAdjust,TransferRequest
from app.dependencies.auth import current_user,require_roles
from app.services.inventory import adjust,get_locked
router=APIRouter(prefix='/inventory',tags=['Inventory'])
@router.post('',status_code=201)
def create(data:InventoryCreate,db:Session=Depends(get_db),user:User=Depends(require_roles('admin','warehouse_manager'))):
    inv=Inventory(**data.model_dump());db.add(inv);db.commit();db.refresh(inv);return inv
@router.get('')
def list_inventory(warehouse_id:int|None=None,product_id:int|None=None,low_stock:bool=False,db:Session=Depends(get_db),user:User=Depends(current_user)):
    q=select(Inventory)
    if warehouse_id:q=q.where(Inventory.warehouse_id==warehouse_id)
    if product_id:q=q.where(Inventory.product_id==product_id)
    if low_stock:q=q.where((Inventory.quantity-Inventory.reserved_quantity)<=Inventory.reorder_threshold)
    return db.scalars(q).all()
@router.post('/{warehouse_id}/{product_id}/adjust')
def adjust_inventory(warehouse_id:int,product_id:int,data:InventoryAdjust,db:Session=Depends(get_db),user:User=Depends(require_roles('admin','warehouse_manager'))):
    adjust(db,warehouse_id,product_id,data.amount,data.reason,user.id);db.commit();return {'message':'inventory adjusted'}
@router.post('/transfer')
def transfer(data:TransferRequest,db:Session=Depends(get_db),user:User=Depends(require_roles('admin','warehouse_manager'))):
    from sqlalchemy import select
    from app.db.models.inventory import Inventory
    ids=sorted([data.source_warehouse_id,data.destination_warehouse_id])
    rows=db.scalars(select(Inventory).where(Inventory.warehouse_id.in_(ids),Inventory.product_id==data.product_id).order_by(Inventory.warehouse_id).with_for_update()).all()
    if len(rows)!=2: from app.core.exceptions import DomainError; raise DomainError('INVENTORY_NOT_FOUND','Inventory records required for both warehouses',404)
    by_id={r.warehouse_id:r for r in rows}; src=by_id[data.source_warehouse_id]; dst=by_id[data.destination_warehouse_id]
    available=src.quantity-src.reserved_quantity
    if available<data.quantity: from app.core.exceptions import DomainError; raise DomainError('INSUFFICIENT_INVENTORY','Insufficient available stock',409)
    src.quantity-=data.quantity;dst.quantity+=data.quantity
    from app.db.models.inventory import InventoryTransaction,InventoryTransactionType
    db.add_all([InventoryTransaction(product_id=data.product_id,warehouse_id=src.warehouse_id,transaction_type=InventoryTransactionType.TRANSFER_OUT,quantity=data.quantity,user_id=user.id,reference_entity='warehouse_transfer',reference_id=f'{src.warehouse_id}-{dst.warehouse_id}'),InventoryTransaction(product_id=data.product_id,warehouse_id=dst.warehouse_id,transaction_type=InventoryTransactionType.TRANSFER_IN,quantity=data.quantity,user_id=user.id,reference_entity='warehouse_transfer',reference_id=f'{src.warehouse_id}-{dst.warehouse_id}')]);db.commit();return {'message':'transfer completed'}
