import csv
import os
from dotenv import load_dotenv
load_dotenv()

def extract():
    files = {
        "customers": os.getenv("LINKCUSTOMER"),
        "products": os.getenv("LINKPRODUCT"),
        "sellers": os.getenv("LINKSELLER"),
        "orders": os.getenv("LINKORDER"),
        "order_items": os.getenv("LINKORDERITEM")
    }
    data = {}
    for table_name, file_path in files.items():
        with open(file_path, "r", encoding="utf-8") as file:
            data[table_name] = list(
                csv.DictReader(file)
            )
    return data