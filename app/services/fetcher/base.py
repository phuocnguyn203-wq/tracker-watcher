from dataclasses import dataclass

@dataclass
class PriceResult():
    success: bool
    final: int
    currency: str | None
    error: str | None
    is_free: bool = False
    
    
    initial_formatted: str | None = None
    final_formatted: str | None = None
    