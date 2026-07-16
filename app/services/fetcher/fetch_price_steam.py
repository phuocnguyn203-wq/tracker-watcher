from app.services.fetcher.base import PriceResult
import requests

BASE_ENDPOINT = 'https://store.steampowered.com/api/appdetails'

def fetch_steam_price_by_id(
    product_id: int,
    cc: str = 'vn'
):
    params = {
        'appids': product_id,
        'cc': cc,
    }
    r = requests.get(
        BASE_ENDPOINT,
        params=params,
    )
    json_r = r.json()[str(product_id)]
    
    is_success = json_r['success']
    
    data = json_r['data']
    
    is_free = data['is_free']
    if is_free:
        return PriceResult(
            success=is_success,
            final=0,
            currency=None,
            error=None,
            is_free=True
        )
    
    #steam multiply price by 100 for every cc
    price_overview = data['price_overview']
    currency = price_overview['currency']
    final = price_overview['final'] / 100
    initial_formatted = price_overview['initial_formatted']
    final_formatted = price_overview['final_formatted']
    return PriceResult(
            success=is_success,
            final=int(final),
            currency=currency,
            error=None,
            is_free=False,
            
            initial_formatted=initial_formatted,
            final_formatted=final_formatted
        )