from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.warehouse import Warehouse,WarehouseAccess
from app.db.models.user import User
from app.schemas.warehouse import WarehouseCreate,WarehouseOut
from app.dependencies.auth import require_roles,current_user
router=APIRouter(prefix='/warehouses',tags=['Warehouses'])
@router.post('',response_model=WarehouseOut,status_code=201)
def create(data:WarehouseCreate,db:Session=Depends(get_db),_=Depends(require_roles('admin'))):
    w=Warehouse(**data.model_dump());db.add(w);db.commit();db.refresh(w);return w
@router.get('',response_model=list[WarehouseOut])
def list_all(db:Session=Depends(get_db),user:User=Depends(current_user)):
    if user.role.value=='admin': return db.scalars(select(Warehouse)).all()
    ids=select(WarehouseAccess.warehouse_id).where(WarehouseAccess.user_id==user.id)
    return db.scalars(select(Warehouse).where(Warehouse.id.in_(ids))).all()
@router.post('/{warehouse_id}/access/{user_id}',status_code=201)
def grant(warehouse_id:int,user_id:int,db:Session=Depends(get_db),_=Depends(require_roles('admin'))):
    if not db.get(Warehouse,warehouse_id) or not db.get(User,user_id): raise HTTPException(404,'Resource not found')
    db.add(WarehouseAccess(warehouse_id=warehouse_id,user_id=user_id));db.commit();return {'message':'access granted'}
