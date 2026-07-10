import pandas as pd
from datetime import datetime

# Lam sach du lieu (chuan hoa,fillna, deduplicate)
#lam sach products
def clean_products(rows):

    df = pd.DataFrame(rows)
    df["category"] = df["category"].str.strip().str.title().fillna("Unknown")
    df["brand"] = df["brand"].str.strip().str.title().fillna("Unknown")

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

    df = df.drop_duplicates(subset=["customer_id"])

    return df.to_dict("records")

#lam sach orders_items
def clean_order_items(rows):
    df = pd.DataFrame(rows)
    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)
    df["discount"] = df["discount"].fillna(0).astype(float)

    df = df.drop_duplicates(subset=["order_id"])

    return df.to_dict("records")

#lam sach orders
def clean_orders(rows):
    df = pd.DataFrame(rows)
    #parse date
    df["order_date"]= df["order_date"].str.replace("/", "-")
    df["ship_date"]= df["ship_date"].str.replace("/", "-")

    df["order_date"] =pd.to_datetime(df["order_date"], format='%Y-%m-%d',errors='coerce')
    df["ship_date"] = pd.to_datetime(df["ship_date"], format='%Y-%m-%d',errors='coerce')

    df = df.dropna(subset=["order_date", "ship_date"]) #loai bo cac dong co order_date hoac ship_date la NaT

    df = df.drop_duplicates(subset=["order_id"])

    return df.to_dict("records")


