import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os
from src.utility.helpers import read_query
load_dotenv()

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 2000)

def read_db(config_data,dir_path):
    type = config_data['type'].lower()
    if type == 'sqlserver':
        if config_data['transformation'][0] == 'Y':
            query = read_query(dir_path)

            print("query", query)
            conn = pyodbc.connect(
                f"DRIVER={os.getenv('DRIVER')};"
                f"SERVER={os.getenv('SERVER')};"
                f"DATABASE={os.getenv('DATABASE')};"
                f"UID={os.getenv('UID')};"
                f"PWD={os.getenv('PASSWORD')};"
            )

            df = pd.read_sql(query, conn)


        else:
            conn = pyodbc.connect(
                f"DRIVER={os.getenv('DRIVER')};"
                f"SERVER={os.getenv('SERVER')};"
                f"DATABASE={os.getenv('DATABASE')};"
                f"UID={os.getenv('UID')};"
                f"PWD={os.getenv('PASSWORD')};"
            )
            query = f"""select * from {config_data['table']}"""
            df = pd.read_sql(query, conn)

    elif type == 'snowflake':
        pass

    return df

