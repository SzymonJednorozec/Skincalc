from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import database
from dto import TestSchema
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/", response_model=TestSchema)
def test_endpoint(db: Session = Depends(get_db)):
    return {"id":1,"name":"test_name"}
    

# def test_endpoint(db: Session = Depends(get_db))