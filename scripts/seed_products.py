"""Insert sample products after the initial migration."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal
from app.models import Product


def main():
    db = SessionLocal()
    try:
        if db.query(Product).count() > 0:
            print("Products already exist, skipping seed.")
            return
        db.add_all(
            [
                Product(
                    title="Laptop",
                    price=999.99,
                    count=5,
                    description="Portable computer",
                ),
                Product(
                    title="Mouse",
                    price=29.99,
                    count=50,
                    description="Wireless mouse",
                ),
            ]
        )
        db.commit()
        print("Inserted 2 products.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
