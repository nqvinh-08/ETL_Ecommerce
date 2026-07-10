import clickhouse_connect
import os
from dotenv import load_dotenv
load_dotenv()

def get_client():
    """
        tao va tra ve ket noi db clickhouse lay gia tri tu .env
        return : ket noi voi db
    """
    return clickhouse_connect.get_client(
    host=os.getenv("HOST"),
    port=int(os.getenv("PORT")),
    username=os.getenv("CLICKHOUSE_USERNAME"),
    password=os.getenv("CLICKHOUSE_PASSWORD"),
    database=os.getenv("CLICKHOUSE_DATABASE")
)