import httpx
from bs4 import BeautifulSoup
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

def scrape_steam_market(page_count: int):
    scraped_items_info = []

    for i in range(0,page_count*10,10):
        url = f'https://steamcommunity.com/market/search?appid=730&start={i}'

        try:
            response = httpx.get(url,headers=headers, timeout=10.0)
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
        
        time.sleep(2)
    return scraped_items_info