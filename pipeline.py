import sys
import os
# đảm bảo import đúng project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from extract.extract_csv import extract
from transform.clean_data import clean_customers, clean_products, clean_sellers, clean_orders, clean_order_items
from dotenv import load_dotenv
load_dotenv()

from load.load_stg import load_stg_table
from load.load_dim import (
    load_dim_customer,
    load_dim_date,
    load_dim_product,
    load_dim_seller
)
from load.load_fact import load_fact


def run_pipeline():
    print("\n START PIPELINE\n")

    #EXTRACT
    raw_data = extract()
    print("Extract done")

    #TRANSFORM
    customers = clean_customers(raw_data["customers"])
    products = clean_products(raw_data["products"])
    sellers = clean_sellers(raw_data["sellers"])
    orders = clean_orders(raw_data["orders"])
    order_items = clean_order_items(raw_data["order_items"])
    print("Transform done")

    # LOAD DATA VAO BANG STG 
    load_stg_table(raw_data["customers"], "stg_customer")
    load_stg_table(raw_data["products"], "stg_product")
    load_stg_table(raw_data["sellers"], "stg_seller")
    load_stg_table(raw_data["orders"], "stg_order")
    load_stg_table(raw_data["order_items"], "stg_order_item")
    print("STG loaded")

    #LOAD VAO BANG DIM
    dim_customer = load_dim_customer(customers)
    dim_product = load_dim_product(products)
    dim_seller = load_dim_seller(sellers)
    dim_date = load_dim_date(orders)
    dim = {
        "customer": dim_customer,
        "product": dim_product,
        "seller": dim_seller,
        "date": dim_date
    }
    print("DIM loaded")

    input_cleaned = {
        "customers": customers,
        "products": products,
        "sellers": sellers,
        "orders": orders,
        "order_items": order_items
    }
    #LOAD VAO BANG FACT
    load_fact(input_cleaned, dim)
    print("FACT loaded")

    print("\n ETL xong\n")

# chay pipeline khi goi file nay truc tiep
if __name__ == "__main__":
    run_pipeline()