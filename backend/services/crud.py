from models import Prices, Items, Markets, ExchangeRate
import datetime
from sqlalchemy.orm import Session
from typing import List

def database_upsert(item_list: List, db: Session, market_name: str):

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
                    price=clean_price,
                    update_date=timestamp
                )
                db.add(new_price)

        except Exception as e:
            print(f"Error for {item_data.get('name')}: {e}")
            db.rollback() 
            continue

    
    db.commit()
    print(f"Zakończono upsert dla {len(item_list)} przedmiotów.")