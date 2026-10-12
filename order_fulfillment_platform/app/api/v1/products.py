from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.product import Product
from app.db.models.user import Role
from app.schemas.product import ProductCreate,ProductOut
from app.dependencies.auth import require_roles
router=APIRouter(prefix='/products',tags=['Products'])
@router.post('',response_model=ProductOut,status_code=201)
def create(data:ProductCreate,db:Session=Depends(get_db),_=Depends(require_roles(Role.ADMIN.value))):
    if db.scalar(select(Product).where(Product.sku==data.sku)): raise HTTPException(409,'SKU already exists')
    p=Product(**data.model_dump());db.add(p);db.commit();db.refresh(p);return p
@router.get('',response_model=list[ProductOut])
def list_products(skip:int=0,limit:int=50,active:bool|None=None,db:Session=Depends(get_db),_=Depends(require_roles('admin','warehouse_manager','fulfillment_agent'))):
    q=select(Product).offset(skip).limit(min(limit,100));
    if active is not None:q=q.where(Product.is_active==active)
    return db.scalars(q).all()
