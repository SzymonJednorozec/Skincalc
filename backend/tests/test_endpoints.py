import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app, get_db
from models import Items, Markets, ExchangeRate, Prices

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_overrides(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.clear()

def test_scrape_steam_items_success(db_session):
    db_session.add(Markets(name="STEAM", fee=0.0))
    db_session.add(ExchangeRate(name="USD", rate=4.0))
    db_session.commit()

    mock_data = [{"name": "Case", "price": "10.00", "img_url": "url"}]
    with patch("main.scrape_steam_market", new_callable=AsyncMock) as mock_scrape:
        mock_scrape.return_value = mock_data
        response = client.get("/api/scrape-steam")
        
    assert response.status_code == 200
    assert response.json()["message"] == "Items and steam prices upserted succesfully"

def test_get_currency_ratio_success(db_session):
    with patch("main.get_exchange_rate", new_callable=AsyncMock) as mock_rate:
        mock_rate.return_value = 4.25
        response = client.get("/api/get-currency-ratio")
    
    assert response.status_code == 200
    assert "updated to 4.25" in response.json()["message"]
    
    rate_in_db = db_session.query(ExchangeRate).filter_by(name="USD").first()
    assert rate_in_db.rate == 4.25

def test_get_all_items_logic(db_session):
    m1 = Markets(name="STEAM", fee=0.0)
    m2 = Markets(name="SKINPORT", fee=0.12)
    item = Items(name="Knife", image_url="url")
    db_session.add_all([m1, m2, item])
    db_session.flush()

    p1 = Prices(item_id=item.id, market_id=m1.id, price=100.0)
    p2 = Prices(item_id=item.id, market_id=m2.id, price=200.0)
    db_session.add_all([p1, p2])
    db_session.commit()

    response = client.get("/api/get-items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Knife"
    assert data[0]["ratio_percentage"] == 176.0 # (200 * 0.88 / 100) * 100

def test_update_item_row_endpoint(db_session):
    db_session.add(Markets(name="STEAM", fee=0.0))
    db_session.add(Markets(name="SKINPORT", fee=0.12))
    db_session.add(ExchangeRate(name="USD", rate=1.0))
    db_session.commit()

    with patch("main.scrape_single_item_steam", new_callable=AsyncMock) as m_steam, \
         patch("main.get_skinport_sales_history", new_callable=AsyncMock) as m_port:
        
        m_steam.return_value = [{"name": "AWP", "price": "100.0", "img_url": "url"}]
        m_port.return_value = [{"name": "AWP", "price": "100.0", "img_url": "url"}]
        
        response = client.post("/api/update-item", json="AWP")

    assert response.status_code == 200
    assert response.json()["name"] == "AWP"

def test_get_currency_ratio_external_failure():
    with patch("main.get_exchange_rate", new_callable=AsyncMock) as mock_rate:
        mock_rate.return_value = None
        response = client.get("/api/get-currency-ratio")
    
    assert response.json()["message"] == "External API failure"
