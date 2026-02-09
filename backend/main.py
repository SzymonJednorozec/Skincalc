from fastapi import FastAPI, Depends, HTTPException
import database
from dto import TestSchema

app = FastAPI()

# database.Base.metadata.create_all(bind=database.engine)

# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@app.get("/", response_model=TestSchema)
def test_endpoint():
    return {"id":1,"name":"test_name"}

# def test_endpoint(db: Session = Depends(get_db))