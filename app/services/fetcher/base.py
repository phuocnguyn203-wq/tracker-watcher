from dataclasses import dataclass

@dataclass
class PriceResult():
    success: bool
    price: int | None
    currency: str | None
    error: str | None
    is_free: bool = False
    