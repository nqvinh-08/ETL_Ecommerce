import csv
import os
from dotenv import load_dotenv
load_dotenv()

#DOC DU LIEU TU FILE CSV
def extract():
    """
        doc du lieu tu file csv trong env.
        return : dictionary chua du lieu cua tung bang
    """
    files = {
        "customers": os.getenv("FILECUSTOMER"),
        "products": os.getenv("FILEPRODUCT"),
        "sellers": os.getenv("FILESELLER"),
        "orders": os.getenv("FILEORDER"),
        "order_items": os.getenv("FILEORDERITEM")
    }
    data = {}
    for table_name, file_path in files.items():
        with open(file_path, "r", encoding="utf-8") as file:
            data[table_name] = list(
                csv.DictReader(file)
            )
    return data