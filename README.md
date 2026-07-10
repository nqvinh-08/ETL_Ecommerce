## Project description
    Du an ETL du lieu su dung pandas:
        Extract data from file CSV 
        --> Load to table STG (data raw)
        --> Transform (chuan hoa du lieu, xu li Null,deduplicate)
        --> Load to table Dim/ Fact (Load new Data, dung batch)
## Project structure
    project
    ├── extract/        #lay du lieu
    ├── transform/      #lam sach du lieu
    ├── load/           #luu dlieu
    └── pipeline.py     #lay-->lam sach-->luu
## Installation && ETL Pipeline

    ### 1. Clone project
        git clone <https://github.com/nqvinh-08/ETL_HeThongThuongMai.git>
    ### 2. Setup environment
        .env
    ### 3.venv (virtual environment)
        python3 -m venv venv (cai moi truong ao)
        source venv/bin/activate (vao moi truong ao)
    ###2.dotenv
        pip install python-dotenv
    ###4.pandas
        pip install pandas
    ###5.clickhouse
        pip install clickhouse-connect
    ###4.Run ETL manually:  
        python3 pipeline.py
