from datetime import date

from sqlalchemy import text
from sqlalchemy.orm import Session


def ensure_sales_seed_data(db: Session) -> None:
    db.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                order_id VARCHAR(64) NOT NULL,
                order_date DATE NOT NULL,
                region VARCHAR(64) NOT NULL,
                state VARCHAR(64),
                revenue NUMERIC(12,2) NOT NULL,
                customers INTEGER DEFAULT 1
            )
            """
        )
    )

    existing = db.execute(text("SELECT COUNT(*) FROM sales")).scalar() or 0
    if existing > 0:
        db.commit()
        return

    seed_rows = [
        ("ORD-1001", date(2025, 1, 5), "North", "New York", 124500.0, 141),
        ("ORD-1002", date(2025, 1, 8), "South", "Texas", 139200.0, 156),
        ("ORD-1003", date(2025, 2, 2), "North", "Illinois", 132800.0, 149),
        ("ORD-1004", date(2025, 2, 10), "South", "Florida", 146400.0, 162),
        ("ORD-1005", date(2025, 3, 3), "North", "Ohio", 141300.0, 165),
        ("ORD-1006", date(2025, 3, 14), "South", "Georgia", 153900.0, 174),
        ("ORD-1007", date(2025, 4, 4), "West", "California", 167200.0, 181),
        ("ORD-1008", date(2025, 4, 18), "East", "Massachusetts", 158300.0, 169),
        ("ORD-1009", date(2025, 5, 7), "West", "Washington", 172400.0, 188),
        ("ORD-1010", date(2025, 5, 23), "East", "Virginia", 161500.0, 176),
        ("ORD-1011", date(2025, 6, 6), "North", "Michigan", 149100.0, 170),
        ("ORD-1012", date(2025, 6, 21), "South", "North Carolina", 164800.0, 182),
    ]

    db.execute(
        text(
            """
            INSERT INTO sales (order_id, order_date, region, state, revenue, customers)
            VALUES (:order_id, :order_date, :region, :state, :revenue, :customers)
            """
        ),
        [
            {
                "order_id": row[0],
                "order_date": row[1],
                "region": row[2],
                "state": row[3],
                "revenue": row[4],
                "customers": row[5],
            }
            for row in seed_rows
        ],
    )
    db.commit()
