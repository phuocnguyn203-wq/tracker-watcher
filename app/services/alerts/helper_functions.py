from app.models.models import Watcher
from app.services.fetcher.base import PriceResult

def should_notify(
    watcher: Watcher,
    price_result: PriceResult
):
    if watcher.target_price >= price_result.final:
        if not watcher.last_state:
            return True
    return False