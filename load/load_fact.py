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

# LOAD VAO BANG FACT(gop 2 bang order va order_item) 
def load_fact(stg, dim):

    df_item = pd.DataFrame(stg["order_items"])
    df_order = pd.DataFrame(stg["orders"])

    # merge 2 bang order_item va orders
    df= df_item.merge(
        df_order[
            ["order_id","customer_id","order_date"]
        ],
        on="order_id",
        how="left"
    )

    #lấy dữ liệu từ db , vì neu khong lay o db thi khi chạy lần 2 mà khoogn có dữ liệu mới thì sẽ trả về là rỗng 
    df_dim_customer = client.query_df("select customer_id,customer_sk from dim_customer")
    df_dim_product = client.query_df("select product_sk, product_id from dim_product")


    # df_dim_customer = pd.DataFrame(dim["customer"])
    # df_dim_product = pd.DataFrame(dim["product"])


    #merge du lieu tu df_dim_product , giu lai tat ca du lieu cua df, lay product_sk cua bang df_dim_product
    df =df.merge(
        df_dim_product[
            ["product_id", "product_sk"]
        ],
        on="product_id",
        how="left"
    )
    #merge du lieu tu df_dim_customer
    df =df.merge(
        df_dim_customer[
            ["customer_id", "customer_sk"]
        ],
        on="customer_id",
        how="left"
    )
    df["date_sk"] = (
        pd.to_datetime(df["order_date"])
        .dt.strftime("%Y%m%d")
        .astype("Int32")
    )

    df =df.dropna(subset=["product_sk","customer_sk"])
    df["product_sk"] = df["product_sk"].astype(int)
    df["customer_sk"] = df["customer_sk"].astype(int)

    df["revenue"] = df["quantity"] * df["unit_price"] - df["discount"]
    df["revenue"] = df["revenue"].round(2).astype(float)

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
    
    #chi lay du lieu moi
    df_new = client.query_df("select order_id from fact_order")
    fact_df = fact_df[
        ~fact_df["order_id"].isin(df_new["order_id"])
    ]
    
    client.insert_df("fact_order", fact_df)