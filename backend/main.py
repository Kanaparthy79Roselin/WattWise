from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from db.session import get_db
from db.session import engine
from db.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="wattwise backend")

@app.get("/")
def health_check():
    return {"status":"wattwise backend is running"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    return {"db": "connected"}
