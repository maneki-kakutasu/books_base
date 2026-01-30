# create_tables.py
from app.database import init_db

if __name__ == "__main__":
    try:
        init_db()
        print("База данных готова к работе!")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")