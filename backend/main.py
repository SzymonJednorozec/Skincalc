from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import database
from dto import TestSchema
from fastapi.middleware.cors import CORSMiddleware
import models
from typing import List

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

@app.get("/", response_model=List[TestSchema])
def test_endpoint(db: Session = Depends(get_db)):
    items = db.query(models.Test).all()
    return items

@app.post("/",response_model=TestSchema)
def test_postendpoint(item: TestSchema,db: Session = Depends(get_db)):
    new_db_item = models.Test()
    new_db_item.name = item.name

    db.add(new_db_item)
    db.commit()
    db.refresh(new_db_item)

    return new_db_item

@app.delete("/")
def test_deleteendpoint(item_id: int,db: Session = Depends(get_db)):
    item = db.query(models.Test).filter(models.Test.id==item_id).first()
    if item:
        db.delete(item)
        db.commit()
        return {"status": "success"}
    

# def test_endpoint(db: Session = Depends(get_db))