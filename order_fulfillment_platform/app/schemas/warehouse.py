from pydantic import BaseModel, Field
class WarehouseCreate(BaseModel): name: str; location: str; capacity: int=Field(gt=0); is_active: bool=True
class WarehouseOut(WarehouseCreate): id: int
