from sqlalchemy import select, inspect, desc, func
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.db import SessionLocal
from app.models.database import Product, ProductAnalysisCache, Review
from app.repositories.product_repo import get_products_from_db
from app.repositories.review_repo import get_reviews_from_db

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
    reviews_count = dict(session.execute((select(Review.root, func.count(Review.id)).group_by(Review.root))).all())
    return templates.TemplateResponse(request, "products.html", {"products": products, "reviews_count": reviews_count})

@app.get("/products/{root}")
def product_detail(request: Request, root: int, session: Session = Depends(get_session)):
    templates = Jinja2Templates(directory="app/web/templates")
    product = session.scalar(select(Product).where(Product.root == root))

    if product is None:
        raise HTTPException(status_code=404)

    aggregate = session.get(ProductAnalysisCache, product.root)
    if aggregate is not None:
        mapper = inspect(ProductAnalysisCache).mapper
        aggregate = {col.key: getattr(aggregate, col.key) for col in mapper.columns}
        aggregate = sorted(aggregate["aggregate"].items(), key=lambda x: x[1]["pos"] + x[1]["neg"], reverse=True)
    
    reviews = get_reviews_from_db(session, root=root, order_by=desc(Review.created_date))

    return templates.TemplateResponse(request, "product_card.html", {"product": product, "aggregate": aggregate, "reviews": reviews})