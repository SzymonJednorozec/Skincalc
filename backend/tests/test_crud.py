
from backend.models import Items, Markets, Prices, ExchangeRate
from backend.services.crud import database_upsert, get_item_row
from backend.services.enums import Market as MarketEnum


def test_database_upsert_insert(db_session):
    new_market = Markets(name=MarketEnum.SKINPORT.value, fee=0.12)
    db_session.add(new_market)
    
    usd_rate = ExchangeRate(name="USD", rate=4.0)
    db_session.add(usd_rate)
    db_session.commit()

    item_list = [
        {
            "name": "AK-47 | Safari Mesh",
            "price": "$5.50 USD",
            "img_url": "http://img.com/ak47.png"
        },
    ]

    database_upsert(item_list, db_session, MarketEnum.SKINPORT.value)

    
    db_item = db_session.query(Items).filter(Items.name == "AK-47 | Safari Mesh").first()
    assert db_item is not None
    assert db_item.name == "AK-47 | Safari Mesh"
    assert db_item.image_url == "http://img.com/ak47.png"

    db_price = db_session.query(Prices).filter(Prices.item_id == db_item.id).first()
    assert db_price is not None
    
    #  5.50 * 4.0 (rate) = 22.0
    assert db_price.price == 22.0
    assert db_price.market_id == new_market.id

    # price_after_fee
    # 22.0 * (1 - 0.12) = 22.0 * 0.88 = 19.36
    assert round(db_item_price_after_fee(db_price), 2) == 19.36

def db_item_price_after_fee(price_obj):
    return price_obj.price_after_fee


def test_database_upsert_update(db_session):
    new_market = Markets(name=MarketEnum.SKINPORT.value, fee=0.12)
    db_session.add(new_market)
    
    usd_rate = ExchangeRate(name="USD", rate=4.0)
    db_session.add(usd_rate)
    db_session.commit()
    
    list1 = [{"name": "Glock", "price": "$1.00", "img_url": "url1"}]
    database_upsert(list1, db_session, MarketEnum.SKINPORT.value)
    
    list2 = [{"name": "Glock", "price": "$2.00", "img_url": "url2"}]
    database_upsert(list2, db_session, MarketEnum.SKINPORT.value)
    
    item = db_session.query(Items).filter(Items.name == "Glock").first()
    price = db_session.query(Prices).filter(Prices.item_id == item.id).first()
    
    assert item.image_url == "url2"  
    assert price.price == 8.0        # (2.0 * 4.0)
    assert db_session.query(Items).count() == 1  




def test_get_item_row_calculates_correct_ratio(db_session):
    item = Items(name="AK-47 | Safari Mesh", image_url="http://img.com")
    db_session.add(item)
    db_session.flush()

    steam_m = Markets(name="STEAM", fee = 0)
    skinport_m = Markets(name="SKINPORT",fee = 0.12)
    db_session.add_all([steam_m, skinport_m])
    db_session.flush()

    p_steam = Prices(item_id=item.id, market_id=steam_m.id, price=100.0)
    p_skinport = Prices(item_id=item.id, market_id=skinport_m.id, price=110.0)
    db_session.add_all([p_steam, p_skinport])
    db_session.commit()

    result = get_item_row("AK-47 | Safari Mesh", db_session)

    assert result["name"] == "AK-47 | Safari Mesh"
    assert result["steam_price"] == 100.0
    # (110 * 0.88 = 96.8), ratio = (96.8 / 100) * 100 = 96.8
    assert result["ratio_percentage"] == 96.8