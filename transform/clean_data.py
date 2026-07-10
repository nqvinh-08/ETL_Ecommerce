import pandas as pd
from datetime import datetime

#lam sach products
def clean_products(rows):
    """
        chuan hoa du lieu, fillna, deduplicate
        args: 
            rows(list[dict]): du lieu goc
        return :
            list[dict]: du lieu da duoc lam sach 
    """
    df_products = pd.DataFrame(rows)
    df_products["category"] = df_products["category"].str.strip().str.title().fillna("Unknown")
    df_products["brand"] = df_products["brand"].str.strip().str.title().fillna("Unknown")

    df_products = df_products.drop_duplicates(subset=["product_id"])

    return df_products.to_dict("records")

# lam sach sellers
def clean_sellers(rows):
    """
        chuan hoa du lieu theo map , fillna, deduplicate
        args: 
            rows(list[dict]): du lieu goc
        return :
            list[dict]: du lieu da duoc lam sach 
    """
    city_map = {
        "hanoi": "Hanoi",
        "ha noi": "Hanoi",
        "hcm": "Ho Chi Minh",
        "ho chi minh": "Ho Chi Minh",
        "da nang": "Da Nang",
        "hai phong": "Hai Phong"
    }
    df_seller= pd.DataFrame(rows)

    df_seller["seller_name"] = df_seller["seller_name"].str.strip().str.title().fillna("Unknown")
    df_seller["city"] = df_seller["city"].str.strip().str.lower().map(city_map).fillna("Unknown")

    df_seller = df_seller.drop_duplicates(subset=["seller_id"])

    return df_seller.to_dict("records") 

#lam sach customers
def clean_customers(rows):
    """
        chuan hoa du lieu theo map , fillna, deduplicate
        args: 
            rows(list[dict]): du lieu goc
        return :
            list[dict]: du lieu da duoc lam sach 
    """
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
    df_customer = pd.DataFrame(rows)
    df_customer["customer_name"] = df_customer["customer_name"].str.strip().str.title().fillna("Unknown")
    df_customer["gender"] = df_customer["gender"].str.strip().str.lower().map(gender_map).fillna("Unknown")
    df_customer["city"] = df_customer["city"].str.strip().str.lower().map(city_map).fillna("Unknown")
    df_customer["segment"] = df_customer["segment"].str.strip().str.title().fillna("Regular")

    df_customer = df_customer.drop_duplicates(subset=["customer_id"])

    return df_customer.to_dict("records")

#lam sach orders_items(ep kieu)
def clean_order_items(rows):
    """
        chuan hoa du lieu , fillna, deduplicate
        args: 
            rows(list[dict]): du lieu goc
        return :
            list[dict]: du lieu da duoc lam sach 
    """
    df_order_items = pd.DataFrame(rows)
    df_order_items["quantity"] = df_order_items["quantity"].fillna(0).astype(int)
    df_order_items["unit_price"] = df_order_items["unit_price"].fillna(0).astype(float)
    df_order_items["discount"] = df_order_items["discount"].fillna(0).astype(float)

    df_order_items = df_order_items.drop_duplicates(subset=["order_id"])

    return df_order_items.to_dict("records")

#lam sach orders(chuyen / --> - va ep kieu format)
def clean_orders(rows):
    """
        chuan hoa du lieu , dropna, deduplicate,ep kieu format
        args: 
            rows(list[dict]): du lieu goc
        return :
            list[dict]: du lieu da duoc lam sach 
    """
    df_order = pd.DataFrame(rows)
    #parse date
    df_order["order_date"]= df_order["order_date"].str.replace("/", "-")
    df_order["ship_date"]= df_order["ship_date"].str.replace("/", "-")

    df_order["order_date"] =pd.to_datetime(df_order["order_date"], format='%Y-%m-%d',errors='coerce')
    df_order["ship_date"] = pd.to_datetime(df_order["ship_date"], format='%Y-%m-%d',errors='coerce')

    #loai bo cac dong co order_date hoac ship_date la NaT
    df_order = df_order.dropna(subset=["order_date", "ship_date"]) 

    df_order = df_order.drop_duplicates(subset=["order_id"])

    return df_order.to_dict("records")


