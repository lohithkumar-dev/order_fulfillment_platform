from pydantic import BaseModel, Field
from app.db.models.return_model import ReturnStatus
class ReturnItemCreate(BaseModel): product_id:int; quantity:int=Field(gt=0)
class ReturnCreate(BaseModel): order_id:int; reason:str=Field(min_length=2,max_length=500); items:list[ReturnItemCreate]=Field(min_length=1)
class ReturnStatusUpdate(BaseModel): status: ReturnStatus
