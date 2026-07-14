from pydantic import BaseModel, Field

class CreateWatcher(BaseModel):
    name: str
    
    source_type: str
    product_id: int
    
    cc: str
    target_price: int
    
    interval_minutes: int
    last_state: bool = Field(default=False)
    