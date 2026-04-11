import httpx

async def get_skinport_sales_history(market_hash_name: str):
    params = {
        "app_id": 730,
        "currency": "PLN",
        "market_hash_name": market_hash_name
    }
    
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(
            "https://api.skinport.com/v1/sales/history", 
            params=params, 
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Błąd {response.status_code}: {response.text}")
            return []
            
        raw_data = response.json()
        items_info = []

        for item in raw_data:
            hash_name = item.get("market_hash_name", "N/A")
            last_24_h = item.get("last_24_hours")
            price = last_24_h.get("median") if last_24_h else None
            
            price_str = str(price) if price is not None else "N/A"
            items_info.append({
                "name": hash_name, 
                "price": price_str, 
                "img_url": None
            })
            
    return items_info



async def get_exchange_rate():
    url = 'https://api.nbp.pl/api/exchangerates/rates/a/usd/'

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url=url,headers=headers)
        if response.status_code!=200:
            print(f"Error: {response.status_code}: {response.text}")
        response.raise_for_status()
        
        data = response.json()
        return data['rates'][0]['mid']