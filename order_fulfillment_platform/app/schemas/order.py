from decimal import Decimal
from pydantic import BaseModel, Field
from app.db.models.order import OrderStatus, PaymentStatus
class OrderItemCreate(BaseModel): product_id:int; quantity:int=Field(gt=0); discount:Decimal=Field(default=0,ge=0); tax:Decimal=Field(default=0,ge=0)
class OrderCreate(BaseModel): warehouse_id:int; items:list[OrderItemCreate]=Field(min_length=1)
class StatusUpdate(BaseModel): status: OrderStatus
class OrderOut(BaseModel): id:int; order_number:str; customer_id:int; warehouse_id:int; total_amount:Decimal; status:OrderStatus; payment_status:PaymentStatus
class AssignOrder(BaseModel): agent_id:int
