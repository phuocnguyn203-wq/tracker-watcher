from app.services.alerts.base import AlertResult

from sqlalchemy.orm import Session
from app.models.models import Watcher

from app.services.fetcher.fetch_price_steam import fetch_steam_price_by_id
from app.services.alerts import helper_functions
from app.services.alerts.notify_dev_terminal import notify_dev_terminal

from datetime import datetime, timezone

def check_watcher(
    db: Session,
    watcher: Watcher
):
    price_result = fetch_steam_price_by_id(
        watcher.product_id
    )
    
    is_notify = helper_functions.should_notify(
        watcher=watcher,
        price_result=price_result,
    )
    if is_notify:
        last_price = watcher.last_price
        
        watcher_name = watcher.name
        
        source_type = watcher.source_type 
        product_id = watcher.product_id
        
        new_last_price = price_result.final
        discount_percent = price_result.discount_percent
        initial_formatted = price_result.initial_formatted
        final_formatted = price_result.final_formatted
        
        message = (
            "[bold green]🔔 PRICE ALERT[/bold green]\n"
            f"Watcher      : [cyan]{watcher_name}[/cyan]\n"
            f"Source       : {source_type}\n"
            f"Product ID   : {product_id}\n"
            f"Last Price   : [yellow]{last_price}[/yellow]\n"
            f"Steam Price  : [green]{final_formatted}[/green]\n"
            f"Original     : [dim]{initial_formatted}[/dim]\n"
            f"Discount     : [bold magenta]{discount_percent}%[/bold magenta]"
        )
                
        notif_result = notify_dev_terminal(message)
        
        watcher.last_state = True
        watcher.last_price = new_last_price
        watcher.last_checked_at = datetime.now(timezone.utc)
        db.commit()
        
        return AlertResult(
            watcher_id=watcher.id,
            price_result=price_result,
            is_triggered=True,
            notification=notif_result,
            error=None
        )

