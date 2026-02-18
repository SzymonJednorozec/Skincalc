from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TestSchema(BaseModel):
    id: int
    name: str

class item_row(BaseModel):
    name: str
    image_url: Optional[str] = None
    steam_price: float
    steam_updated: datetime
    skinport_price: float
    sell_price_after_fee: float
    skinport_updated: datetime
    ratio_percentage: float

    class Config:
        from_attributes = True