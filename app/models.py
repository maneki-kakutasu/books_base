from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Product(Base):
    """Каноническая модель книги после дедупликации"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String(20), unique=True, index=True, nullable=True)
    title = Column(String(500), nullable=False, index=True)
    author = Column(String(500), index=True)
    description = Column(Text)
    image_url = Column(String(1000))
    publisher = Column(String(255))
    year = Column(Integer)
    genre = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    offers = relationship("Offer", back_populates="product", cascade="all, delete-orphan")
    attributes = relationship("ProductAttribute", back_populates="product")

class Offer(Base):
    """Конкретные предложения от магазинов (Labirint, Book24 и т.д.)"""
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    
    website_name = Column(String(100))
    price = Column(Float)
    old_price = Column(Float, nullable=True)
    url = Column(String(1000))
    availability = Column(Boolean, default=True)
    date_parsed = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="offers")

class ProductAttribute(Base):
    """Дополнительные характеристики книги"""
    __tablename__ = "attributes"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    
    name = Column(String(255))
    value = Column(String(500))

    product = relationship("Product", back_populates="attributes")