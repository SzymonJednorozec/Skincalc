from database import SessionLocal
from models import Markets

def seed_markets():
    db = SessionLocal()
    try:
        initial_markets = [
            {"name": "STEAM", "fee": 0.0},
            {"name": "SKINPORT", "fee": 0.08}
        ]

        for m in initial_markets:
            exists = db.query(Markets).filter(Markets.name == m["name"]).first()
            if not exists:
                new_market = Markets(name=m["name"], fee=m["fee"])
                db.add(new_market)
                print(f"Dodano market: {m['name']}")
        
        db.commit()
    except Exception as e:
        print(f"Błąd: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_markets()