import json
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Product, Offer, ProductAttribute

def import_from_json(file_path: str):
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return

    db: Session = SessionLocal()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Начинаем импорт {len(data)} записей...")

    for entry in data:
        isbn = entry.get('isbn')
        if not isbn:
            continue

        # 1. Проверяем, есть ли уже такая книга в таблице products (Дедупликация)
        product = db.query(Product).filter(Product.isbn == isbn).first()

        if not product:
            # Если книги нет, создаем новый Product
            product = Product(
                isbn=isbn,
                title=entry.get('title'),
                author=entry.get('author'),
                description=entry.get('description'),
                image_url=entry.get('image_url'),
                publisher=entry.get('publisher'),
                year=entry.get('year')
            )
            db.add(product)
            db.flush() # Получаем ID нового продукта

        # 2. Создаем предложение (Offer) от конкретного сайта
        # Проверяем, нет ли уже такого же предложения (чтобы не дублировать при повторном запуске)
        existing_offer = db.query(Offer).filter(
            Offer.product_id == product.id, 
            Offer.website_name == entry.get('website_name'),
            Offer.price == entry.get('price')
        ).first()

        if not existing_offer:
            new_offer = Offer(
                product_id=product.id,
                website_name=entry.get('website_name'),
                price=entry.get('price'),
                url=entry.get('url')
            )
            db.add(new_offer)

    db.commit()
    db.close()
    print("Импорт завершен успешно!")

if __name__ == "__main__":
    files_to_import = [
        ('Book24', 'data/book24_raw.json'),
        ('Читай-Город', 'data/chitai_gorod_raw.json')
    ]
    
    for name, path in files_to_import:
        print(f"\n>>> Загрузка данных из {name}...")
        import_from_json(path)