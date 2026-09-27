from sqlalchemy import select, inspect, desc
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.db import SessionLocal
from app.models.database import Product, ProductAnalysisCache
from app.repositories.product_repo import get_products_from_db

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")

def get_session():
    with SessionLocal() as session:
        yield session

@app.get("/")
def index():
    return {"status": "ok"}

@app.get("/products")
def products_list(request: Request, session: Session = Depends(get_session)):
    templates = Jinja2Templates(directory="app/web/templates")
    products = get_products_from_db(session, count=1000, order_by=desc(Product.feedbacks_count))
    return templates.TemplateResponse(request, "products.html", {"products": products})

@app.get("/products/{root}")
def product_detail(request: Request, root: int, session: Session = Depends(get_session)):
    templates = Jinja2Templates(directory="app/web/templates")
    product = session.scalar(select(Product).where(Product.root == root))
    mapper = inspect(ProductAnalysisCache).mapper
    aggregate = session.get(ProductAnalysisCache, product.root)
    if aggregate is not None:
        aggregate = {col.key: getattr(aggregate, col.key) for col in mapper.columns}
    return templates.TemplateResponse(request, "product_card.html", {"product": product, "aggregate": aggregate})