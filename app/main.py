from fastapi import FastAPI, Request, Depends, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from .database import get_db
from .models import Product, Offer

app = FastAPI(title="Book Integrator")

# Настройка шаблонов (создадим папку templates позже)
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def index(request: Request, db: Session = Depends(get_db), q: str = Query(None)):
    """Главная страница со строкой поиска и списком книг"""
    if q:
        # Поиск по названию или автору (независимо от регистра)
        products = db.query(Product).filter(
            (Product.title.ilike(f"%{q}%")) | (Product.author.ilike(f"%{q}%"))
        ).all()
    else:
        # Если поиска нет, показываем последние 20 книг
        products = db.query(Product).limit(20).all()
        
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "products": products,
        "query": q
    })

@app.get("/product/{product_id}")
def product_detail(request: Request, product_id: int, db: Session = Depends(get_db)):
    """Страница конкретной книги со всеми предложениями"""
    product = db.query(Product).filter(Product.id == product_id).first()
    return templates.TemplateResponse("product.html", {
        "request": request, 
        "product": product
    })