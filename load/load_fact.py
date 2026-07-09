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

# LOAD VAO BANG FACT
def load_fact(stg, dim):
    df = pd.DataFrame(stg["order_items"])

    customer_map = {
        c["customer_id"]: c["customer_sk"]
        for c in dim["customer"]
    }

    product_map = {
        p["product_id"]: p["product_sk"]
        for p in dim["product"]
    }
    #chuyen sang string--> int
    df["date_sk"] = df["order_date"].dt.strftime("%Y%m%d").astype(int)

    #chuan hoa du lieu, fillna, ep kieu 
    df["customer_sk"] = (
        df["customer_id"]
        .map(customer_map)
        .fillna(0)
        .astype(int)
    )
    df["product_sk"] = (
        df["product_id"]
        .map(product_map)
        .fillna(0)
        .astype(int)
    )
    df["discount"] =(
        df["discount"]
        .interpolate() #uoc luong gia tri
        .astype(float)
    ) 
    df["revenue"] = df["quantity"] * df["unit_price"] - df["discount"]

    fact_df = df[
        [
            "order_id",
            "date_sk",
            "customer_sk",
            "product_sk",
            "quantity",
            "unit_price",
            "discount",
            "revenue"
        ]
    ]
    client.insert_df("fact_order", fact_df)
    print("FACT loaded")