from pydantic import BaseModel, Field
from datetime import datetime

class CreateWatcher(BaseModel):
    name: str
    
    source_type: str
    product_id: int
    
    cc: str
    target_price: int
    
    interval_minutes: int
    last_state: bool = Field(default=False)

class ReturnedWatcher(BaseModel):
    id: int
    
    user_id: int
    
    name: str
    
    source_type: str
    product_id: int

    cc: str
    target_price: int

    interval_minutes: int
    last_state: bool = Field(default=False)
    last_price: int | None = None
    last_checked_at: datetime | None = None

class UpdateWatcher(BaseModel):
    name: str
    
    source_type: str
    product_id: int

    cc: str
    target_price: int

    interval_minutes: int
    last_state: bool = Field(default=False)
    last_price: int | None = None
    last_checked_at: datetime | None = None
    
    