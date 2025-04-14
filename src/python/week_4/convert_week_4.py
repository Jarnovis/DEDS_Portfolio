# %% [markdown]
# # DEDS WC 4.2

# %% [markdown]
# ## Imports

# %%
import pandas as pd
import sqlite3 as sql3
import pyodbc
from settings import logger, settings
import os
import os
print(os.path.exists("C:/Users/jdvis_x5odeao/Semester_4/DEDS_Portfolio/data/raw/go_crm_train.sqlite"))

# %% [markdown]
# ## Connecties sqlite databases

# %%
crm_conn = sql3.connect("C:/Users/jdvis_x5odeao/Semester_4/DEDS_Portfolio/data/raw/go_crm_train.sqlite")
sales_conn = sql3.connect("C:/Users/jdvis_x5odeao/Semester_4/DEDS_Portfolio/data/raw/go_sales_volledig.sqlite")
staff_conn = sql3.connect("C:/Users/jdvis_x5odeao/Semester_4/DEDS_Portfolio/data/raw/go_staff_volledig.sqlite")

# %% [markdown]
# ## Connectie SDM

# %%
DB = {
    "servername" : r"VISSIE\SQLEXPRESS",
    "database" : "SDM"}

export_conn = pyodbc.connect(f"""DRIVER={'SQL SERVER'};
                             SERVER={DB['servername']};
                             DATABASE={DB['database']};
                             Trusted_Connection=yes
                             """)

export_conn.setencoding('utf-8')
export_conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
export_conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')

export_cursor = export_conn.cursor()

# %% [markdown]
# ## Automatische dataframes

# %%
def create_dataframes_sql(connection, db_type : str):
    dictionary : dict = {}
    query : str = ""
    key : str = ""
    
    if (db_type == "sqlite"):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        key = "name"
    elif (db_type == "ssms"):
        query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';"
        key = "TABLE_NAME"
    else:
        return {}
    table_names = pd.read_sql(query, connection)
    
    for table in table_names[key].tolist():
        dictionary[table] = pd.read_sql(f"SELECT * FROM {table}", connection)
    
    return dictionary

def create_dataframes_csv(path, name, seperator):
    frame = pd.read_csv(path, sep=seperator)
    
    return {name : frame}

# %% [markdown]
# ## Uitlezen connecties pandas

# %%
forecast_updated = create_dataframes_csv("C:/Users/jdvis_x5odeao/Semester_4/DEDS_Portfolio/data/raw/updated_product_forecast_volledig.csv", "forecast", ",")
inventory_updated = create_dataframes_csv("C:/Users/jdvis_x5odeao/Semester_4/DEDS_Portfolio/data/raw/updated_inventory_levels_volledig.csv", "inventory", ";")
database = create_dataframes_sql(export_conn, "ssms")
crm = create_dataframes_sql(crm_conn, "sqlite")
sales = create_dataframes_sql(sales_conn, "sqlite")
staff = create_dataframes_sql(staff_conn, "sqlite")

# %% [markdown]
# Alleen de unique lines blijven over

# %% [markdown]
# Alleen de unique linens blijven over

# %% [markdown]
# ## 

# %%

# %% [markdown]
# ## Insert code

# %%
def sql_convertes(table: str, frame: pd.DataFrame):
    insert_statements = []

    for _, row in frame.iterrows():
        columns = ', '.join(row.index)
        values = ', '.join([
            f"'{value.replace("'", "''")}'" if isinstance(value, str) else "NULL" if pd.isna(value) else str(value)
            for value in row
        ])
        insert_statement = f"INSERT INTO {table} ({columns}) VALUES ({values});"
        insert_statements.append(insert_statement)

    return insert_statements


def main():
    new_rows : dict = {}
    insert_statement = []

    database["forecast"] = pd.concat([database["forecast"], forecast_updated["forecast"]], ignore_index=True)

    new_rows["forecast"] = database["forecast"][~database["forecast"].duplicated(keep=False)]

    database["inventory_levels"] = pd.concat([database["inventory_levels"], inventory_updated["inventory"]], ignore_index=True)
    database["inventory_levels"]

    new_inventories = database["inventory_levels"][~database["inventory_levels"].duplicated(keep=False)]

    new_rows["inventory_levels"] = new_inventories

    # %%
    for name, frame in crm.items():
        database[name] = pd.concat([database[name], frame], ignore_index=True)
        new_rows[name] = database[name][~database[name].duplicated(keep=False)]

    for name, frame in sales.items():
        database[name] = pd.concat([database[name], frame], ignore_index=True)
        new_rows[name] = database[name][~database[name].duplicated(keep=False)]

    for name, frame in staff.items():
        database[name] = pd.concat([database[name], frame], ignore_index=True)
        new_rows[name] = database[name][~database[name].duplicated(keep=False)]
    
    for name, frame in new_rows.items():
        insert_statement += sql_convertes(name, frame)
    
    duplicated_keys = 0

    for statement in insert_statement:
        try:
            export_cursor.execute(statement)
        except pyodbc.Error as e:
            duplicated_keys += 1
            print(e)
        

    print(len(insert_statement))
    print(f"{duplicated_keys} rows not comitted")

# %% [markdown]
# ## Forecast ids toevoegen

# %%
def ids():
    file_path = r"..\..\..\data\raw\inventory_levels_volledig.csv" 
    df = pd.read_csv(file_path, sep=';')  

    df.insert(1, 'INVENTORY_ID', range(len(df)))

    df.to_csv(r"..\..\..\data\raw\updated_inventory_levels_volledig.csv", index=False, sep=';') 

    print("DONE: INVENTORY_ID added with semicolon format.")



