import pandas as pd
def batch_insert(
    client,
    table_name,
    df,
    batch_size = 5
):
    """
        insert vao db theo tung batch
        args:
            client:ket noi clickhouse
            table_name(str): ten bang 
            df(dataframe): du lieu can insert
            batch_size(int) :so dong moi lan insert
        return : None 
    """
    if df.empty:
        return
    total = len(df)
    for i in range(0, total, batch_size):
        batch = df.iloc[i : i + batch_size]
        client.insert_df(
            table_name,
            batch
        )