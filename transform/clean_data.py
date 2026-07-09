import pandas as pd
from datetime import datetime

# Lam sach du lieu (chuan hoa, deduplicate)
#lam sach products
def clean_products(rows):

    df = pd.DataFrame(rows)
    df["category"] = df["category"].str.strip().str.title().fillna("Unknown")
    df["brand"] = df["brand"].str.strip().str.title().fillna("Unknown")
    if not df["product_id"].is_unique:
        df = df.drop_duplicates(subset=["product_id"])

    return df.to_dict("records")

# lam sach sellers
def clean_sellers(rows):

    city_map = {
        "hanoi": "Hanoi",
        "ha noi": "Hanoi",
        "hcm": "Ho Chi Minh",
        "ho chi minh": "Ho Chi Minh",
        "da nang": "Da Nang",
        "hai phong": "Hai Phong"
    }
    df= pd.DataFrame(rows)

    df["seller_name"] = df["seller_name"].str.strip().str.title().fillna("Unknown")
    df["city"] = df["city"].str.strip().str.lower().map(city_map).fillna("Unknown")
    if not df["seller_id"].is_unique:
        df = df.drop_duplicates(subset=["seller_id"])

    return df.to_dict("records") 

#lam sach customers
def clean_customers(rows):
    gender_map = {
        "m": "Male", "male": "Male",
        "f": "Female", "female": "Female",
        "nam": "Male", "nu": "Female", "nữ": "Female"
    }

    city_map = {
        "hanoi": "Hanoi",
        "ha noi": "Hanoi",
        "hcm": "Ho Chi Minh",
        "ho chi minh": "Ho Chi Minh",
        "da nang": "Da Nang",
        "hai phong": "Hai Phong"
    }
    df = pd.DataFrame(rows)
    df["customer_name"] = df["customer_name"].str.strip().str.title().fillna("Unknown")
    df["gender"] = df["gender"].str.strip().str.lower().map(gender_map).fillna("Unknown")
    df["city"] = df["city"].str.strip().str.lower().map(city_map).fillna("Unknown")
    df["segment"] = df["segment"].str.strip().str.title().fillna("Regular")
    if not df["customer_id"].is_unique:
        df = df.drop_duplicates(subset=["customer_id"])

    return df.to_dict("records")

#lam sach orders_items
def clean_order_items(rows):
    df = pd.DataFrame(rows)
    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)
    df["discount"] = df["discount"].fillna(0).astype(float)
    if not df["order_id"].is_unique:
        df = df.drop_duplicates(subset=["order_id"])

    return df.to_dict("records")

#lam sach orders
def clean_orders(rows):
    df = pd.DataFrame(rows)
    #parse date
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"] = pd.to_datetime(df["ship_date"])
    if not df["order_id"].is_unique:
        df = df.drop_duplicates(subset=["order_id"])

    return df.to_dict("records")


