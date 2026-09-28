import pandas as pd

from sqlalchemy import text

from app.db.database import engine


def get_orders():
    query = text("""
        SELECT
            o.order_id,
            o.order_date,
            c.customer_name,
            p.product_name,
            o.quantity,
            o.revenue,
            o.cost
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        JOIN products p
            ON o.product_id = p.product_id
        ORDER BY o.order_date;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        orders = [
            dict(row._mapping)
            for row in result
        ]

    return orders


def get_total_revenue():
    query = text("""
        SELECT COALESCE(SUM(revenue), 0) AS total_revenue
        FROM orders;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        row = result.fetchone()

    print("DATABASE RESULT:", row)
    print("REVENUE VALUE:", row._mapping["total_revenue"])

    return float(row._mapping["total_revenue"])

def get_montly_revenue():
    query = text("""
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(revenue) AS revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
    ORDER BY month;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        monthly_revenue = [
            dict(row._mapping)
            for row in result
        ]

    return monthly_revenue

def get_monthly_profit():
    query = text("""
        SELECT
            DATE_TRUNC('month', order_date) AS month,
            SUM(revenue - cost) AS profit
        FROM orders
        GROUP BY DATE_TRUNC('month', order_date)
        ORDER BY month;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        monthly_profit = [
            dict(row._mapping)
            for row in result
        ]

    return monthly_profit

def get_monthly_revenue_pandas():
    query = """
        SELECT
            order_date,
            revenue
        FROM orders;
    """

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    df["order_date"] = pd.to_datetime(df["order_date"])

    df["month"] = df["order_date"].dt.to_period("M")

    monthly_revenue = (
        df.groupby("month")["revenue"]
        .sum()
        .reset_index()
    )

    monthly_revenue["month"] = monthly_revenue["month"].astype(str)

    return monthly_revenue.to_dict(orient="records")