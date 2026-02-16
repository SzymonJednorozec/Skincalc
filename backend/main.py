from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import database
from dto import TestSchema
from fastapi.middleware.cors import CORSMiddleware
from models import Prices, Items, Markets, ExchangeRate
from typing import List
from fastapi import Body
from backend.services.external_api import get_skinport_sales_history,get_exchange_rate
from services.utils import get_market_hash_chunks
from services.crud import database_upsert
from services.scraper import scrape_steam_market
import asyncio


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

database.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get("/", response_model=List[TestSchema])
# def test_endpoint(db: Session = Depends(get_db)):
#     items = db.query(models.Test).all()
#     return items

# @app.post("/",response_model=TestSchema)
# def test_postendpoint(item: str = Body(...),db: Session = Depends(get_db)):
#     new_db_item = models.Test()
#     new_db_item.name = item

#     db.add(new_db_item)
#     db.commit()
#     db.refresh(new_db_item)

#     return new_db_item

# @app.delete("/")
# def test_deleteendpoint(item_id: int,db: Session = Depends(get_db)):
#     item = db.query(models.Test).filter(models.Test.id==item_id).first()
#     if item:
#         db.delete(item)
#         db.commit()
#         return {"status": "success"}
    
@app.get("/api")
async def test_api(db: Session = Depends(get_db)):
    await get_exchange_rate()
    

@app.get("/api/sync-skinport")
async def sync_skinport_prices(db: Session = Depends(get_db)):
    items_from_db = db.query(Items).all()
    if not items_from_db:
        return {"message": "Items table empty"}

    formated_names = [item.name for item in items_from_db]

    name_chunks = get_market_hash_chunks(formated_names)

    for names in name_chunks:
        try:
            data = await get_skinport_sales_history(names)
            database_upsert(data,db,"SKINPORT")
            await asyncio.sleep(1)

        except Exception as e:
            print({f"Unexpected error {e}"})
            continue

    return {"message": "Skinport prices updated"}

@app.get("/api/scrape-steam")
async def scrape_steam_items(db: Session = Depends(get_db)):
    items_from_steam = await scrape_steam_market(5)
    if not items_from_steam:
        return {"message": "Scraper failure"}
    
    try:
        database_upsert(items_from_steam,db,"STEAM")
    except Exception as e:
        print({f"Unexpected error {e}"})
    return {"message": "Items and steam prices upsertet succesfully"}

@app.get("/api/get-currency-ratio")
async def get_currency_ratio(db: Session = Depends(get_db)):
    exchange_rate = await get_exchange_rate() 
    if not exchange_rate:
        return {"message": "External API failure"}
    
    try:
        db_usd = db.query(ExchangeRate).filter(ExchangeRate.name=="USD").first()
        if not db_usd:
            new_usd = ExchangeRate(name = "USD", rate = exchange_rate)
            db.add(new_usd)
        else:
            db_usd.rate = exchange_rate
        db.commit()
    except Exception as e:
        db.rollback()
        print({f"Unexpected error {e}, db changes have been rolled back"})
        return {"message": "Database update failed"}
    
    return {"message": f"Currency ratio updated to {exchange_rate}"}
    