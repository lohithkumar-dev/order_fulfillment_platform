from fastapi import APIRouter,Depends,HTTPException,Header
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.order import Order,OrderStatus
from app.db.models.idempotency import IdempotencyKey
from app.schemas.order import OrderCreate,OrderOut,StatusUpdate,AssignOrder
from app.dependencies.auth import current_user,require_roles
from app.services.order import create_order,change_status
from app.services.audit import audit
from app.services.notification import notify
router=APIRouter(prefix='/orders',tags=['Orders'])
@router.post('',response_model=OrderOut,status_code=201)
def create(data:OrderCreate,idempotency_key:str|None=Header(None),db:Session=Depends(get_db),user:User=Depends(require_roles('customer'))):
    if idempotency_key:
        old=db.scalar(select(IdempotencyKey).where(IdempotencyKey.user_id==user.id,IdempotencyKey.key==idempotency_key))
        if old: return old.response_body
    order=create_order(db,user.id,data.warehouse_id,data.items);audit(db,user.id,'order_created','order',order.id);notify(db,user.id,'ORDER_CREATED',f'Order {order.order_number} created');db.commit();db.refresh(order)
    result={'id':order.id,'order_number':order.order_number,'customer_id':order.customer_id,'warehouse_id':order.warehouse_id,'total_amount':order.total_amount,'status':order.status,'payment_status':order.payment_status}
    if idempotency_key: db.add(IdempotencyKey(user_id=user.id,key=idempotency_key,response_status=201,response_body=result));db.commit()
    return result
@router.get('',response_model=list[OrderOut])
def list_orders(status:OrderStatus|None=None,warehouse_id:int|None=None,skip:int=0,limit:int=50,db:Session=Depends(get_db),user:User=Depends(current_user)):
    q=select(Order).offset(skip).limit(min(limit,100))
    if user.role.value=='customer':q=q.where(Order.customer_id==user.id)
    if status:q=q.where(Order.status==status)
    if warehouse_id:q=q.where(Order.warehouse_id==warehouse_id)
    return db.scalars(q).all()
@router.post('/{order_id}/status',response_model=OrderOut)
def status(order_id:int,data:StatusUpdate,db:Session=Depends(get_db),user:User=Depends(require_roles('admin','fulfillment_agent','warehouse_manager'))):
    o=db.get(Order,order_id)
    if not o:raise HTTPException(404,'Order not found')
    change_status(db,o,data.status,user.id);audit(db,user.id,'order_status_changed','order',o.id,{'to':data.status.value});db.commit();db.refresh(o);return o
@router.post('/{order_id}/assign',response_model=OrderOut)
def assign(order_id:int,data:AssignOrder,db:Session=Depends(get_db),user:User=Depends(require_roles('admin','warehouse_manager'))):
    o=db.get(Order,order_id);agent=db.get(User,data.agent_id)
    if not o or not agent:raise HTTPException(404,'Order or agent not found')
    if agent.role.value!='fulfillment_agent' or not agent.is_active:raise HTTPException(400,'Invalid or inactive agent')
    o.fulfillment_agent_id=agent.id
    if o.status==OrderStatus.CONFIRMED: change_status(db,o,OrderStatus.ASSIGNED,user.id)
    audit(db,user.id,'order_assigned','order',o.id,{'agent_id':agent.id});notify(db,agent.id,'ORDER_ASSIGNED',f'Order {o.order_number} assigned');db.commit();db.refresh(o);return o
@router.post('/{order_id}/cancel',response_model=OrderOut)
def cancel(order_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    o=db.get(Order,order_id)
    if not o or (user.role.value=='customer' and o.customer_id!=user.id):raise HTTPException(404,'Order not found')
    change_status(db,o,OrderStatus.CANCELLED,user.id);audit(db,user.id,'order_cancelled','order',o.id);notify(db,o.customer_id,'ORDER_CANCELLED',f'Order {o.order_number} cancelled');db.commit();db.refresh(o);return o
