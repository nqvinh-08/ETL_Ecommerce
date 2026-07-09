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

#LOAD VAO BANG DIM 

# dim_customer
def load_dim_customer(stg_customers):

    df = pd.DataFrame(stg_customers).copy()
    df = df [
        [
            "customer_id",
            "customer_name", 
            "gender", 
            "city", 
            "segment"
        ]
    ]
    df.insert(0, "customer_sk", range(1, len(df) + 1)) #them cot customer_sk vao vi tri 0, gia tri tu 1 den len(df)

    client.insert_df("dim_customer", df)
    return df.to_dict("records")


#dim_product
def load_dim_product(stg_products):

    df = pd.DataFrame(stg_products).copy()
    df = df[
        [
            "product_id",
            "product_name",
            "category",
            "brand"
        ]
    ]
    df.insert(0, "product_sk", range(1, len(df) + 1)) #them cot product_sk vao vi tri 0, gia tri tu 1 den len(df)

    client.insert_df("dim_product", df)
    return df.to_dict("records")


#dim_seller
def load_dim_seller(stg_sellers):
    df = pd.DataFrame(stg_sellers).copy()
    df = df[
        [
            "seller_id",
            "seller_name",
            "city"
        ]
    ]
    df.insert(0, "seller_sk", range(1, len(df) + 1)) #them cot seller_sk vao vi tri 0, gia tri tu 1 den len(df)

    client.insert_df("dim_seller", df)
    return df.to_dict("records")

#dim_date
def load_dim_date(stg_orders):
    df = pd.DataFrame(stg_orders).copy()
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce" #gia tri khong hop le se tra ve NaT
    )
    df =df [
        [
            "date",
            "year",
            "month",
            "day",
        ]
    ]
    df.insert(0, "date_sk", range(1, len(df) + 1)) #them cot date_sk vao vi tri 0, gia tri tu 1 den len(df)
    client.insert_df("dim_date", df)
    return df.to_dict("records")