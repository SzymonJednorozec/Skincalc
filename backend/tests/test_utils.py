import pytest

from backend.services.utils import clean_price

def test_clean_price_polish_format():
    price = "12,74zł"
    rate = 1.0
    result = clean_price(price,rate)
    assert result == 12.74

def test_clean_price_usd_format():
    price="$47.50 USD"
    rate=1.0
    result = clean_price(price,rate)
    assert result == 47.50

def test_clean_price_conversion():
    price="$5.50 USD"
    rate=2.0
    result = clean_price(price,rate)
    assert result == 11.0