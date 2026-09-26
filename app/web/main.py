from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates

from app.db import SessionLocal
from app.repositories.product_repo import load_products_from_db


app = FastAPI()

def get_session():
    with SessionLocal() as session:
        yield session

@app.get("/")
def index():
    return {"status": "ok"}

@app.get("/products")
def products_list(request: Request, session: Session = Depends(get_session)):
    templates = Jinja2Templates(directory="app/web/templates")
    products = load_products_from_db(session, 1000)
    return templates.TemplateResponse(request, "products.html", {"products": products})
