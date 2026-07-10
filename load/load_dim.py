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
    #check du lieu moi do vao co giong du lieu da co khong
    #chi lay du lieu chua co
    df_existing = client.query_df("select customer_id from dim_customer")
    if "customer_id" in df_existing.columns:
        df = df[
            ~df["customer_id"].isin(
                df_existing["customer_id"]
            )
        ]
    if df.empty:
        print("khong co customer moi")
        return []
    
    #tim trong bang dim check da ton tai customer_sk chua
    existing_sk = client.query_df("select customer_sk from dim_customer ")
    #neu tra ve rong
    if existing_sk.empty:
        start_sk=1
    #neu co tim giatri max
    else:
        start_sk = existing_sk["customer_sk"].max() +1

    df.insert(0,"customer_sk", range(start_sk , start_sk+ len(df)))
    
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

    #check du lieu moi do vao co giong du lieu da co khong
    #chi lay du lieu chua co
    df_new = client.query_df("select product_id from dim_product")
    if "product_id" in df_new.columns:
        df = df[
            ~df["product_id"].isin(
                df_new["product_id"]
            )
        ]
    if df.empty:
        print("khong co product moi")
        return []
    
    #tim trong bang dim check da ton tai product_sk chua
    existing_df = client.query_df("select product_sk from dim_product ")
    #neu tra ve rong
    if existing_df.empty:
        start_sk=1
    #neu co tim giatri max
    else:
        start_sk = existing_df["product_sk"].max() +1
    df.insert(0,"product_sk", range(start_sk , start_sk+ len(df)))

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
    #check du lieu moi do vao co giong du lieu da co khong
    #chi lay du lieu chua co
    df_new = client.query_df("select seller_id from dim_seller")
    if "seller_id" in df_new.columns:
        df = df[
            ~df["seller_id"].isin(
                df_new["seller_id"]
            )
        ]
    if df.empty:
        print("khong co seller moi")
        return []
    
    #tim trong bang dim check da ton tai seller_sk chua
    existing_df = client.query_df("select seller_sk from dim_seller ")
    #neu tra ve rong
    if existing_df.empty:
        start_sk=1
    #neu co tim giatri max
    else:
        start_sk = existing_df["seller_sk"].max() +1
    df.insert(0,"seller_sk", range(start_sk , start_sk+ len(df)))

    client.insert_df("dim_seller", df)
    return df.to_dict("records")

#dim_date
def load_dim_date(stg_orders):
    df = pd.DataFrame(stg_orders).copy()

    #tao dim_date voi cac cot year, month, day tu order_date
    dim_date =pd.DataFrame({
        "date_sk": df["order_date"].dt.strftime('%Y%m%d').astype("Int32"),
        "date": df["order_date"].dt.date,
        "year": df["order_date"].dt.year,
        "month": df["order_date"].dt.month,
        "day": df["order_date"].dt.day
        }
    )
    existing_df = client.query_df("select date_sk from dim_date")
    
    dim_date =dim_date.drop_duplicates(subset=["date_sk"])

    client.insert_df("dim_date", dim_date)
    return dim_date.to_dict("records")