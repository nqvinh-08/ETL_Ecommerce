"""
Module load dữ liệu từ STG vào Data Warehouse trên ClickHouse.

Bao gồm:
- Load dữ liệu vào các bảng staging.
- Load dữ liệu vào các bảng dimension.
- Load dữ liệu vào bảng fact_order.
- Sinh surrogate key cho dimension tables.
- Loại bỏ dữ liệu đã tồn tại trước khi insert.
"""

import pandas as pd
from config.database import get_client
from until.batch_insert import batch_insert


#LOAD VAO BANG STG
def load_stg_table(client,df, table_name):
    """
        Load du lieu raw vao bang STG
        Tham so: du lieu tu dataframe
        Return: 
    """
    df = pd.DataFrame(df)
    batch_insert(client,table_name, df)
    print(f"Loaded STG: {table_name}")


#LOAD VAO BANG DIM 
# dim_customer
def load_dim_customer(client,stg_customers):
    """
        Load du lieu vao bang dim_customer
        Loai bo cac customer_id da ton tai , sinh customer_sk moi 
        va insert cac ban ghi moi vao bang dim
        Tham so: stg_customers (dataframe) da duoc lam sach
        return : Danh sach ban ghi moi duoc insert
    """
    df_customer = pd.DataFrame(stg_customers).copy()
    df_customer = df_customer [
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
        df_customer = df_customer[
            ~df_customer["customer_id"].isin(
                df_existing["customer_id"]
            )
        ]
    if df_customer.empty:
        print("khong co customer moi")
        return []
    
    #tim trong bang dim check da ton tai customer_sk chua
    existing_sk = client.query_df("select customer_sk from dim_customer ")

    if existing_sk.empty:
        start_sk=1
    #neu co tim giatri max
    else:
        start_sk = existing_sk["customer_sk"].max() +1

    df_customer.insert(0,"customer_sk", range(start_sk , start_sk+ len(df_customer)))
    
    # client.insert_df("dim_customer", df)
    #insert theo batch( ketnoi clickhouse, ten bang, dataframe)
    batch_insert(client,"dim_customer",df_customer)

    return df_customer.to_dict("records")

#dim_product
def load_dim_product(client,stg_products):
    """
        Load dữ liệu sản phẩm vào bảng dim_product.
        Loại bỏ các product_id đã tồn tại, sinh product_sk mới
        và insert các bản ghi mới vào dimension table.
        Args:
            stg_products (list | DataFrame): Dữ liệu sản phẩm đã được làm sạch.
        Returns:
            list: Danh sách bản ghi mới được insert.
    """
    df_products = pd.DataFrame(stg_products).copy()
    df_products = df_products[
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
        df_products = df_products[
            ~df_products["product_id"].isin(
                df_new["product_id"]
            )
        ]
    if df_products.empty:
        print("khong co product moi")
        return []
    
    #tim trong bang dim check da ton tai product_sk chua
    existing_df = client.query_df("select product_sk from dim_product ")

    if existing_df.empty:
        start_sk=1
    #neu co tim giatri max
    else:
        start_sk = existing_df["product_sk"].max() +1
    df_products.insert(0,"product_sk", range(start_sk , start_sk+ len(df_products)))

    #client.insert_df("dim_product", df_products)
    batch_insert(client , "dim_product", df_products)
    return df_products.to_dict("records")


#dim_seller
def load_dim_seller(client,stg_sellers):
    """
        Load dữ liệu seller vào bảng dim_seller.
        Loại bỏ các seller_id đã tồn tại, sinh seller_sk mới
        và insert các bản ghi mới vào dimension table.
        Args:
            stg_seller (list | DataFrame): Dữ liệu sản phẩm đã được làm sạch.
        Returns:
            list: Danh sách bản ghi mới được insert.
    """
    df_seller = pd.DataFrame(stg_sellers).copy()
    df_seller = df_seller[
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
        df_seller = df_seller[
            ~df_seller["seller_id"].isin(
                df_new["seller_id"]
            )
        ]
    if df_seller.empty:
        print("khong co seller moi")
        return []
    
    #tim trong bang dim check da ton tai seller_sk chua
    existing_df = client.query_df("select seller_sk from dim_seller ")

    if existing_df.empty:
        start_sk=1
    #neu co tim giatri max
    else:
        start_sk = existing_df["seller_sk"].max() +1
    df_seller.insert(0,"seller_sk", range(start_sk , start_sk+ len(df_seller)))

    # client.insert_df("dim_seller", df_seller)
    batch_insert(client,"dim_seller",df_seller)
    return df_seller.to_dict("records")

#dim_date
def load_dim_date(client,stg_orders):
    """
        Tạo và load dữ liệu thời gian vào bảng dim_date.
        Sinh date_sk từ order_date, tách các thuộc tính năm,
        tháng, ngày và loại bỏ các ngày trùng lặp.
        Args:
            stg_orders (list | DataFrame): Dữ liệu đơn hàng.
        Returns:
            list: Danh sách bản ghi ngày tháng được insert.
    """
    df_date = pd.DataFrame(stg_orders).copy()

    #tao dim_date voi cac cot year, month, day tu order_date
    dim_date =pd.DataFrame({
        "date_sk": df_date["order_date"].dt.strftime('%Y%m%d').astype("Int32"),
        "date": df_date["order_date"].dt.date,
        "year": df_date["order_date"].dt.year,
        "month": df_date["order_date"].dt.month,
        "day": df_date["order_date"].dt.day
        }
    )
    
    dim_date =dim_date.drop_duplicates(subset=["date_sk"])

    #check du lieu moi do vao co giong du lieu da co khong
    #chi lay du lieu chua co
    df_new = client.query_df("select date_sk from dim_date")
    if "date_sk" in df_new.columns:
        dim_date = dim_date[
            ~dim_date["date_sk"].isin(
                df_new["date_sk"]
            )
        ]
    if dim_date.empty:
        print("khong co date moi")
        return []
    
    # client.insert_df("dim_date", dim_date)
    batch_insert(client, "dim_date", dim_date)
    return dim_date.to_dict("records")


# LOAD VAO BANG FACT(gop 2 bang order va order_item) 
def load_fact(client,stg):
    """
        Tạo và load dữ liệu vào bảng fact_order.
        Ghép dữ liệu từ orders và order_items, ánh xạ khóa thay thế
        (customer_sk, product_sk), tính doanh thu và chỉ insert
        các đơn hàng chưa tồn tại trong fact_order.
        Args:
            stg (dict): Dữ liệu staging gồm orders và order_items.
        Returns:
            None
    """
    df_item = pd.DataFrame(stg["order_items"])
    df_order = pd.DataFrame(stg["orders"])

    # merge 2 bang order_item va orders
    df_fact= df_item.merge(
        df_order[
            ["order_id","customer_id","order_date"]
        ],
        on="order_id",
        how="left"
    )

    #lấy dữ liệu từ db , vì neu khong lay o db thi khi chạy lần 2 mà khoogn có dữ liệu mới thì sẽ trả về là rỗng 
    df_dim_customer = client.query_df("select customer_id,customer_sk from dim_customer")
    df_dim_product = client.query_df("select product_sk, product_id from dim_product")

    #merge du lieu tu df_dim_product , giu lai tat ca du lieu cua df, lay product_sk cua bang df_dim_product
    df_fact =df_fact.merge(
        df_dim_product[
            ["product_id", "product_sk"]
        ],
        on="product_id",
        how="left"
    )
    #merge du lieu tu df_dim_customer
    df_fact =df_fact.merge(
        df_dim_customer[
            ["customer_id", "customer_sk"]
        ],
        on="customer_id",
        how="left"
    )
    df_fact["date_sk"] = (
        pd.to_datetime(df_fact["order_date"])
        .dt.strftime("%Y%m%d")
        .astype("Int32")
    )

    df_fact =df_fact.dropna(subset=["product_sk","customer_sk"])
    df_fact["product_sk"] = df_fact["product_sk"].astype(int)
    df_fact["customer_sk"] = df_fact["customer_sk"].astype(int)

    df_fact["revenue"] = df_fact["quantity"] * df_fact["unit_price"] - df_fact["discount"]
    df_fact["revenue"] = df_fact["revenue"].round(2).astype(float)

    df_fact = df_fact[
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
    if "order_id" in df_new.columns:
        df_fact = df_fact[
            ~df_fact["order_id"].isin(
                df_new["order_id"]
            )
        ]
    if df_fact.empty:
        print("Khong co fact moi")
        return

    # client.insert_df("fact_order", df_fact)
    batch_insert(client, "fact_order", df_fact)