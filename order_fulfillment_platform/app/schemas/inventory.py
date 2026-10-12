from pydantic import BaseModel, Field
class InventoryCreate(BaseModel): product_id:int; warehouse_id:int; quantity:int=Field(ge=0); reorder_threshold:int=Field(ge=0)
class InventoryAdjust(BaseModel): amount:int; reason:str=Field(min_length=2,max_length=300)
class TransferRequest(BaseModel): product_id:int; source_warehouse_id:int; destination_warehouse_id:int; quantity:int=Field(gt=0)
class InventoryOut(BaseModel): id:int; product_id:int; warehouse_id:int; quantity:int; reserved_quantity:int; reorder_threshold:int
