import pytest

from backend.services.utils import clean_price, get_market_hash_chunks

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

def test_hash_chunks():
    names = ['A','A','A','B','B','B','C','C']
    chunk_size = 3
    result = get_market_hash_chunks(names,chunk_size)
    assert result[0] == "A,A,A"
    assert result[1] == "B,B,B"
    assert result[2] == "C,C"