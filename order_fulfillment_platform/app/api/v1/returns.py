from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.return_model import Return,ReturnItem,ReturnStatus
from app.db.models.order import Order
from app.db.models.user import User
from app.schemas.return_schema import ReturnCreate,ReturnStatusUpdate
from app.dependencies.auth import current_user,require_roles
router=APIRouter(prefix='/returns',tags=['Returns'])
@router.post('',status_code=201)
def create(data:ReturnCreate,db:Session=Depends(get_db),user:User=Depends(require_roles('customer'))):
    o=db.get(Order,data.order_id)
    if not o or o.customer_id!=user.id or o.status.value not in ('delivered',):raise HTTPException(400,'Order is not eligible for return')
    r=Return(order_id=o.id,customer_id=user.id,reason=data.reason);db.add(r);db.flush()
    for i in data.items:db.add(ReturnItem(return_id=r.id,product_id=i.product_id,quantity=i.quantity))
    db.commit();db.refresh(r);return r
@router.post('/{return_id}/status')
def status(return_id:int,data:ReturnStatusUpdate,db:Session=Depends(get_db),user:User=Depends(require_roles('admin','warehouse_manager'))):
    r=db.get(Return,return_id)
    if not r:raise HTTPException(404,'Return not found')
    allowed={ReturnStatus.REQUESTED:{ReturnStatus.APPROVED,ReturnStatus.REJECTED},ReturnStatus.APPROVED:{ReturnStatus.RECEIVED},ReturnStatus.RECEIVED:{ReturnStatus.COMPLETED},ReturnStatus.REJECTED:set(),ReturnStatus.COMPLETED:set()}
    if data.status not in allowed[r.status]:raise HTTPException(409,'Invalid return transition')
    r.status=data.status;db.commit();db.refresh(r);return r
