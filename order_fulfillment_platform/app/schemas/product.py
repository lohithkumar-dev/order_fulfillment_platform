from decimal import Decimal
from pydantic import BaseModel, Field
class ProductCreate(BaseModel): sku: str; name: str; description: str|None=None; category: str|None=None; price: Decimal=Field(ge=0); cost_price: Decimal=Field(ge=0); is_active: bool=True
class ProductOut(ProductCreate): id: int
