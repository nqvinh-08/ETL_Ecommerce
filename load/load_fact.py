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
def load_fact(stg, dim):
    customer_map = {
        c["customer_id"]: c["customer_sk"]
        for c in dim["customer"]
    } # vd:C001: 1 --> truy xuat tuc thoi khong can duyet lai toan bo bang
    product_map = {
        p["product_id"]: p["product_sk"]
        for p in dim["product"]
    }
    order_map = {
        o["order_id"]: o
        for o in stg["orders"]
    }
    fact = []
    for item in stg["order_items"]:
        order = order_map.get(item["order_id"])
        if not order:
            continue
        order_date = pd.to_datetime(
            order["order_date"],
            errors="coerce" #gia tri khong hop le se tra ve NaT
        )
        if pd.isna(order_date):
            continue
        date_sk = int(
            order_date.strftime("%Y%m%d")
        )
        quantity = int(item["quantity"])
        unit_price = float(item["unit_price"])
        discount = float(item["discount"])

        revenue = quantity * unit_price - discount
        fact.append({
            "order_id": item["order_id"],
            "date_sk": date_sk,
            "customer_sk": customer_map.get(
                order["customer_id"], 0
            ), #tra ve customer_sk tuong ung voi customer_id, neu khong co tra ve 0
            "product_sk": product_map.get(
                item["product_id"], 0
            ),
            "quantity": quantity,
            "unit_price": unit_price,
            "discount": discount,
            "revenue": revenue
        })
    fact_df = pd.DataFrame(fact)
    client.command("TRUNCATE TABLE fact_order")
    client.insert_df(
        "fact_order",
        fact_df
    )
    print("✔ FACT loaded")