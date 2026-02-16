import re

def clean_price(price_str: str, exchange_rate: float = 1.0) -> float:
    if not price_str or price_str == "N/A":
        return 0.0

    price_str = price_str.replace(',', '.').replace('\xa0', '').strip() #PLN example: 1,01zł
    match = re.search(r"(\d+\.?\d*)", price_str) #USD example: $47.50 USD
    
    if not match:
        return 0.0

    try:
        value = float(match.group(1))
        
        if any(symbol in price_str.upper() for symbol in ['$', 'USD']):
            return round(value * exchange_rate, 2)
        
        return round(value, 2)

    except ValueError:
        return 0.0
