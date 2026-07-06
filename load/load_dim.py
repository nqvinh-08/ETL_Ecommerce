import pandas as pd
import clickhouse_connect
import os
from dotenv import load_dotenv
load_dotenv()
client = clickhouse_connect.get_client(
    host=os.getenv("HOST"),
    port=int(os.getenv("PORT")),
    username=os.getenv("CLICKHOUSE_USERNAME"),
    password=os.getenv("CLICKHOUSE_PASSWORD"),
    database=os.getenv("CLICKHOUSE_DATABASE")
)

# dim_customer
def load_dim_customer(stg_customers):

    dim = []

    for i, c in enumerate(stg_customers):
        dim.append({
            "customer_sk": i + 1,
            "customer_id": c["customer_id"],
            "customer_name": c["customer_name"],
            "gender": c["gender"],
            "city": c["city"],
            "segment": c["segment"]
        })

    client.insert_df("dim_customer", pd.DataFrame(dim))
    return dim


#dim_product
def load_dim_product(stg_products):

    dim = []

    for i, p in enumerate(stg_products): #enumerate: tra ve index va gia tri
        dim.append({
            "product_sk": i + 1,
            "product_id": p["product_id"],
            "product_name": p["product_name"],
            "category": p["category"],
            "brand": p["brand"]
        })

    client.insert_df("dim_product", pd.DataFrame(dim)) #chuyen list thanh bang --> insert vao dim_products
    return dim


#dim_seller
def load_dim_seller(stg_sellers):

    dim = []

    for i, s in enumerate(stg_sellers):
        dim.append({
            "seller_sk": i + 1,
            "seller_id": s["seller_id"],
            "seller_name": s["seller_name"],
            "city": s["city"]
        })

    client.insert_df("dim_seller", pd.DataFrame(dim))   
    return dim

#dim_date
def load_dim_date(stg_orders):
    df = pd.DataFrame(stg_orders)
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce" #gia tri khong hop le se tra ve NaT
    )
    dates = sorted(
        df["order_date"].dropna().unique() #bo nan, trung
    )
    dim = []
    for d in dates:

        d = pd.Timestamp(d)
        dim.append({
            "date_sk": int(d.strftime("%Y%m%d")),
            "date": d.date(),
            "year": d.year,
            "month": d.month,
            "day": d.day
        })
    client.insert_df(
        "dim_date",
        pd.DataFrame(dim)
    )