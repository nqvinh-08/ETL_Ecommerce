import sys
import os
# đảm bảo import đúng project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from extract.extract_csv import extract
from transform.clean_customers import clean_customers
from transform.clean_order_items import clean_order_items
from transform.clean_sellers import clean_sellers
from transform.clean_products import clean_products
from transform.clean_orders import clean_orders
from dotenv import load_dotenv
load_dotenv()

print(os.getenv("PORT"))
print(os.getenv("CLICKHOUSE_USERNAME"))
print(os.getenv("CLICKHOUSE_PASSWORD"))
print(os.getenv("CLICKHOUSE_DATABASE"))
print(os.getenv("LINKCUSTOMER"))
print(os.getenv("LINKSELLER"))
print(os.getenv("LINKORDER"))
print(os.getenv("LINKORDERITEM"))

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

    #extract
    raw_data = extract()
    print("✔ Extract done")

    #transform
    customers = clean_customers(raw_data["customers"])
    products = clean_products(raw_data["products"])
    sellers = clean_sellers(raw_data["sellers"])
    orders = clean_orders(raw_data["orders"])
    order_items = clean_order_items(raw_data["order_items"])
    print("✔ Transform done")

    # gom lại
    stg_input = {
        "customers": customers,
        "products": products,
        "sellers": sellers,
        "orders": orders,
        "order_items": order_items
    }

    #load stg
    load_stg_table(raw_data["customers"], "stg_customer")
    load_stg_table(raw_data["products"], "stg_product")
    load_stg_table(raw_data["sellers"], "stg_seller")
    load_stg_table(raw_data["orders"], "stg_order")
    load_stg_table(raw_data["order_items"], "stg_order_item")
    print("✔ STG loaded")

    #load dim
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
    print("✔ DIM loaded")

    #load fact
    load_fact(stg_input, dim)
    print("✔ FACT loaded")

    print("\n PIPELINE COMPLETED SUCCESSFULLY\n")
if __name__ == "__main__":
    run_pipeline()