"""
ETL Pipeline cho hệ thống quản lý cửa hàng.
Quy trình:
1. Extract dữ liệu từ file CSV.
2. Transform và làm sạch dữ liệu.
3. Load dữ liệu vào các bảng staging.
4. Load dữ liệu vào các bảng dimension.
5. Load dữ liệu vào bảng fact.
"""
from config.database import get_client
from extract.extract_csv import extract
from transform.clean_data import clean_customers, clean_products, clean_sellers, clean_orders, clean_order_items
from dotenv import load_dotenv
load_dotenv()
from store_data.store_data import(
    load_stg_table,
    load_dim_customer,
    load_dim_date,
    load_dim_product,
    load_dim_seller,
    load_fact
)

def run_pipeline():
    """
        Thực thi toàn bộ quy trình ETL.
        Các bước thực hiện:
        - Extract dữ liệu từ các file CSV.
        - Transform và làm sạch dữ liệu.
        - Load dữ liệu vào các bảng STG.
        - Load dữ liệu vào các bảng Dimension.
        - Load dữ liệu vào bảng Fact.
        Returns:
            None
    """
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

    client = get_client()

    # LOAD DATA VAO BANG STG 
    load_stg_table(client,raw_data["customers"], "stg_customer")
    load_stg_table(client,raw_data["products"], "stg_product")
    load_stg_table(client,raw_data["sellers"], "stg_seller")
    load_stg_table(client,raw_data["orders"], "stg_order")
    load_stg_table(client,raw_data["order_items"], "stg_order_item")
    print("STG loaded")

    #LOAD VAO BANG DIM
    load_dim_customer(client,customers)
    load_dim_product(client,products)
    load_dim_seller(client,sellers)
    load_dim_date(client,orders)
    print("DIM loaded")

    stg = {
        "customers": customers,
        "products": products,
        "sellers": sellers,
        "orders": orders,
        "order_items": order_items
    }
    #LOAD VAO BANG FACT
    load_fact(client,stg)
    print("FACT loaded")

    print("\n ETL xong\n")

# chay pipeline khi goi file nay truc tiep
if __name__ == "__main__":
    run_pipeline()