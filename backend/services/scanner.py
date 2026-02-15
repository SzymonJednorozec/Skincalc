import httpx

async def get_skinport_sales_history():
    params = {
        "app_id": 730,
        "currency": "PLN",
        "market_hash_name": "Glove Case,★ Karambit | Slaughter (Minimal Wear)"
    }
    
    headers = {
        "Accept": "application/json", 
        "Accept-Encoding": "br",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.skinport.com/v1/sales/history", 
            params=params, 
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Błąd {response.status_code}: {response.text}")
        response.raise_for_status()
        
        data = response.json()

        for x in data:
            print(x)
