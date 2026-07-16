from app.services.alerts.base import NotificationResult

from rich import print as rprint

def notify_dev_terminal(
    body: str
) -> NotificationResult:
    rprint(body)
    return NotificationResult(
        is_send_success=True,
        channel='dev_terminal',
        error=None
    )