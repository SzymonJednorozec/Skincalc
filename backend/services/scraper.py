import httpx
from bs4 import BeautifulSoup
import time
import asyncio
import re
from urllib.parse import quote

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

async def scrape_steam_market(page_count: int):
    scraped_items_info = []
    async with httpx.AsyncClient() as client:
        for i in range(0,page_count*10,10):
            url = f'https://steamcommunity.com/market/search?appid=730&start={i}'

            try:
                response = await client.get(url,headers=headers, timeout=10.0)
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                print(f"Error status code: {e.response.status_code} | scrape_steam_market()")
                break
            except Exception as e:
                print(f"Unexpectet error: {e} | scrape_steam_market()")
                break
            
            html = BeautifulSoup(response.text,"html.parser")
            item_row_content = html.find_all('a',class_='market_listing_row_link')

            if not item_row_content:
                print(f"None elements found on page {int(i/10)} | scrape_steam_market()")

            for item in item_row_content:
                row_div = item.find('div', class_='market_recent_listing_row')
                name = row_div.get('data-hash-name') if row_div else "N/A"

                price_span = item.find('span', attrs={'data-price': True})
                price = price_span.get_text(strip=True) if price_span else "N/A"

                img_tag = item.find('img', class_='market_listing_item_img')
                img_url = img_tag['src'] if img_tag else "No image"

                item_info = {"name": name,"price": price,"img_url": img_url}
                scraped_items_info.append(item_info)
            
            await asyncio.sleep(2)
    return scraped_items_info

async def scrape_single_item_steam(hash_name):
    url_page = f"https://steamcommunity.com/market/listings/730/{quote(hash_name)}"
    scraped_item_info = []
    async with httpx.AsyncClient() as client:
        r = await client.get(url_page)
        match = re.search(r'Market_LoadOrderSpread\(\s*(\d+)\s*\)', r.text)
        
        if match:
            item_id = match.group(1)
        
            api_url = f"https://steamcommunity.com/market/itemordershistogram?country=PL&language=polish&currency=6&item_nameid={item_id}"
            api_res = await client.get(api_url)
            data = api_res.json()
            
            if data.get("success") == 1:
                lowest_sell = str(float(data.get('lowest_sell_order', 0)) / 100)
                item_info = {"name": hash_name,"price": lowest_sell,"img_url": None}
                scraped_item_info.append(item_info)
                return scraped_item_info
        return None