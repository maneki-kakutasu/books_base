import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Загружаем переменные из .env
load_dotenv()

# Формируем URL подключения для PostgreSQL
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаем движок SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий для взаимодействия с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Функция для создания таблиц в базе данных"""
    # Base.metadata.create_all создаст все таблицы, описанные в models.py
    Base.metadata.create_all(bind=engine)
    print(f"Таблицы в БД '{DB_NAME}' успешно инициализированы.")

def get_db():
    """Генератор сессий для FastAPI (Dependency Injection)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()