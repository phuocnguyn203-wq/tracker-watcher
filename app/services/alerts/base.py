from dataclasses import dataclass

from app.services.fetcher.base import PriceResult

@dataclass
class NotificationResult:
    is_send_success: bool
    channel: str         # 'email', 'discord', 'dev_terminal', etc
    error: str | None
@dataclass
class AlertResult:
    watcher_id: int
    price_result: PriceResult
    is_triggered: bool
    notification: NotificationResult | None
    error: str | None