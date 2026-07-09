import pandas as pd
import clickhouse_connect
import os
from dotenv import load_dotenv
load_dotenv()

client = clickhouse_connect.get_client(
    host=os.getenv("HOST"),
    port= int(os.getenv("PORT")),
    username=os.getenv("CLICKHOUSE_USERNAME"),
    password=os.getenv("CLICKHOUSE_PASSWORD"),
    database=os.getenv("CLICKHOUSE_DATABASE")
)
#LOAD VAO BANG STG
def load_stg_table(df, table_name):
    df = pd.DataFrame(df)
    client.insert_df(table_name, df)
    print(f"Loaded STG: {table_name}")