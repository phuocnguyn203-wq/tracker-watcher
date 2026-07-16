from dataclasses import dataclass

@dataclass
class PriceResult():
    success: bool
    price: int
    currency: str | None
    error: str | None
    is_free: bool = False
    