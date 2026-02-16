import httpx
from bs4 import BeautifulSoup
import time
from typing import List
from models import Prices, Items, Markets, ExchangeRate
import re
import datetime

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


def database_upsert(page_count: int, db: Session, market_name: str):
    
    item_list = scrape_steam_market(page_count=page_count)
    if not item_list:
        return

    target_market = db.query(Markets).filter(Markets.name == market_name).first()
    if not target_market:
        print(f"Error market {market_name} does not exist")
        return
    
    exchange_rate = db.query(ExchangeRate).filter(ExchangeRate.name=="USD").first()
    if not exchange_rate:
        print(f"Error exchange rate does not exist")
        return
    
    currency_rate = exchange_rate.rate
    timestamp = datetime.now()

    for item_data in item_list:
        try:
            db_item = db.query(Items).filter(Items.name == item_data['name']).first()
            
            if not db_item:
                db_item = Items(name=item_data['name'], image_url=item_data['img_url'])
                db.add(db_item)
                db.flush()  
            else:
                if db_item.image_url != item_data['img_url']:
                    db_item.image_url = item_data['img_url']


            db_price = db.query(Prices).filter(
                Prices.item_id == db_item.id,
                Prices.market_id == target_market.id
            ).first()

            clean_price = clean_price(item_data["price"],currency_rate)

            if db_price:
                db_price.price = clean_price
            else:
                new_price = Prices(
                    item_id=db_item.id,
                    market_id=target_market.id,
                    price=clean_price
                    update_date=timestamp
                )
                db.add(new_price)

        except Exception as e:
            print(f"Error for {item_data.get('name')}: {e}")
            db.rollback() 
            continue

    
    db.commit()
    print(f"Zakończono upsert dla {len(item_list)} przedmiotów.")



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


