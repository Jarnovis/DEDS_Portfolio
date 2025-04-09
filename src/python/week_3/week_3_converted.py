# %% [markdown]
# # DEDS WC 3.2

# %% [markdown]
# ## Imports

# %%
import pyodbc
import sqlite3 as sql
import pandas as pd
import asyncio
import nest_asyncio
from settings import settings, logger

nest_asyncio.apply()

# %% [markdown]
# ## Connectie SSMS

# %%
DB_TOTAL = {
    "servername" : r"VISSIE\SQLEXPRESS",
    "database" : "SDM"}

export_conn_sdm = pyodbc.connect(f"""DRIVER={'SQL SERVER'};
                             SERVER={DB_TOTAL['servername']};
                             DATABASE={DB_TOTAL['database']};
                             Trusted_Connection=yes
                             """)

export_conn_sdm.setencoding('utf-8')
export_conn_sdm.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
export_conn_sdm.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')

export_cursor_sdm = export_conn_sdm.cursor()

DB_GO = {
    "servername" : r"VISSIE\SQLEXPRESS",
    "database" : "GREAT_OUTDOORS"}

export_conn_go = pyodbc.connect(f"""DRIVER={'SQL SERVER'};
                             SERVER={DB_GO['servername']};
                             DATABASE={DB_GO['database']};
                             Trusted_Connection=yes
                             """)

export_conn_go.setencoding('utf-8')
export_conn_go.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
export_conn_go.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')

export_cursor_go = export_conn_go.cursor()

def test_connection(connection):
    try:
        # Attempt a simple query to check if the connection is alive
        connection.execute("SELECT 1")
        print("Connection is alive!")
    except Exception as e:
        print(f"Error connecting: {e}")

test_connection(export_conn_sdm)
test_connection(export_conn_go)



# %% [markdown]
# ## Dataframes

# %%
def create_dataframes_sql(connection):
    dictionary : dict = {}
    query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';"
    key = "TABLE_NAME"
    
    tables = pd.read_sql(query, connection)
    
    for table in tables[key].tolist():
        dictionary[table] = pd.read_sql(f"SELECT * FROM {table}", connection)
    
    return dictionary

sdm_frames = create_dataframes_sql(export_conn_sdm)

# %% [markdown]
# ## Querie makers

# %%
from typing import Iterable

def query_remove(table_name : str):
    try:
        query = f"DELETE FROM {table_name}"
        export_cursor_go.execute(query)
        export_cursor_go.commit()
    except pyodbc.Error as e:
        print(f"ERROR: {table_name}: {e}")
        return table_name
    
    return None

def rigth_type(value, column_name, types):
    dtype = types[column_name]
    
    if pd.isna(value):
        return "NULL"
    
    if dtype == "object" or dtype == "string":
        value = value.replace("'", "''")
        return f"'{value}'"
    
    return f"{value}"
    

def create_add_query(row, types):
    query = ""
    columns = list(row.keys())
    
    for pos in range(len(columns)):
        column_name = columns[pos]
        value = row[column_name]
        
        if (pos == len(columns) - 1):
            query += f"{column_name}) VALUES ("
        else:
            query += f"{column_name}, "
    
    data = list(row)
    
    for pos in range(len(data)):
        column_name = columns[pos]
        value = row[column_name]
        
        if pos == len(columns) - 1:
            query += f"{rigth_type(value, column_name, types)})"
        else:
            query += f"{rigth_type(value, column_name, types)}, "
    
    return query

def query_add(table_name : str, table_data : pd.DataFrame):
    queries = []
    types = table_data.dtypes

    for index, row in table_data.iterrows():
        query : str = f"INSERT INTO {table_name} ("
        query += create_add_query(row, types)
        queries.append(query)
    
    return queries

# %% [markdown]
# ## Leegmaken Great Outdoors database

# %%
def empty_go():
    tables_go : list = [
        "returned_item",
        "order_details",
        "retailer_site",
        "sales_staff",
        "inventory",
        "product_forcast",
        "product",
        "date"
    ]
    
    while len(tables_go) > 0:
        for table in tables_go:
            try:
                temp = query_remove(table)
                
                if (temp == None):
                    tables_go.remove(table)
                    print(f"REMOVED {table}")
                else:
                    print(f"NOT YET REMOVED: {table}")
            except pyodbc.Error as e:
                print(e)
        
    print("All items are removed")

empty_go()

# %% [markdown]
# ## Great Outdoors vullen

# %% [markdown]
# ### Datums converter

# %%
def convert_date(date : str):
    converted = pd.to_datetime(date)
    year = converted.year
    month = converted.month
    quarter = (month - 1 ) // 3 + 1
    converted = converted.strftime("%Y-%m-%d")
    
    return pd.DataFrame({
        "DATE" : [converted], 
        "YEAR" : [year], 
        "MONTH" : [month], 
        "QUARTER" : [quarter]}).astype({
            "YEAR": "Int64",
            "MONTH" : "Int64",
            "QUARTER" : "Int64"
        })

# %% [markdown]
# ### Frames aanmaken
# async methodes voor een snellere verwerkings tijd

# %%
dates_go = pd.DataFrame({
    "DATE" : [],
    "YEAR" : [],
    "QUARTER" : [],
    "MONTH" : []
})

async def create_forecast():
    print("Forecast started")
    await asyncio.sleep(1)
    print("Forecast done")
    return sdm_frames["forecast"]

async def create_inventory():
    print("Invenotry started")
    await asyncio.sleep(1)
    print("Inventory done")
    return sdm_frames["inventory_levels"]

async def create_sales_staff():
    print("sales_staff started")
    await asyncio.sleep(1)
    global dates_go
    sales_staff_go = sdm_frames["sales_staff"]
    
    for index, row in sales_staff_go.iterrows():
        sales_staff_go.at[index, "FULL_NAME"] = f"{row["FIRST_NAME"]} {row["LAST_NAME"]}"
        date_details : pd.DataFrame = convert_date(row["DATE_HIRED"])
        dates_go = pd.concat([dates_go, date_details], ignore_index=True)
    
    print("sales_staff done")    
    return sales_staff_go[["SALES_STAFF_CODE", "POSITION_EN", "WORK_PHONE", "EXTENSION", "FAX", "EMAIL", "DATE_HIRED", "MANAGER_CODE", "FULL_NAME"]]

async def create_retailer_site():
    print("retailer_site started")
    await asyncio.sleep(1)
    retailer_site_go = pd.merge(sdm_frames["retailer_site"], sdm_frames["country"], left_on="COUNTRY_CODE", right_on="COUNTRY_CODE")
    
    print("retailer_site done")
    return retailer_site_go[["RETAILER_SITE_CODE", "ADDRESS1", "ADDRESS2", "CITY", "REGION", "POSTAL_ZONE", "COUNTRY", "ACTIVE_INDICATOR", "CURRENCY_NAME"]].rename(columns={
        "CURRENCY_NAME" : "CURRENCY",
        "COUNTRY" : "COUNTRY_EN"
    })

async def create_product():
    print("product started")
    await asyncio.sleep(1)
    global dates_go
    
    product_go = pd.merge(sdm_frames["product"], sdm_frames["product_type"], left_on="PRODUCT_TYPE_CODE", right_on="PRODUCT_TYPE_CODE")
    product_go = pd.merge(product_go, sdm_frames["product_line"], left_on="PRODUCT_LINE_CODE", right_on="PRODUCT_LINE_CODE")
    product_go = product_go[["PRODUCT_NUMBER", "INTRODUCTION_DATE", "PRODUCTION_COST", "MARGIN", "PRODUCT_IMAGE", "LANGUAGE", "PRODUCT_NAME", "DESCRIPTION", "PRODUCT_TYPE_EN", "PRODUCT_LINE_EN"]].rename(columns={
        "PRODUCT_TYPE_EN" : "PRODUCTION_TYPE_EN",
        "PRODUCT_LINE_EN" : "PRODUCTION_LINE_EN"
    })
    
    for index, row in product_go.iterrows():
        date_details : pd.DataFrame = convert_date(row["INTRODUCTION_DATE"])
        dates_go = pd.concat([dates_go, date_details], ignore_index=True)
    
    print("product done")
    return product_go

async def create_order_details():
    print("order_details started")
    await asyncio.sleep(1)
    global dates_go
    
    order_details_go = pd.merge(sdm_frames["order_details"], sdm_frames["order_header"], left_on="ORDER_NUMBER", right_on="ORDER_NUMBER")
    order_details_go = pd.merge(order_details_go, sdm_frames["order_method"], left_on="ORDER_METHOD_CODE", right_on="ORDER_METHOD_CODE")
    
    for index, row in order_details_go.iterrows():
        order_details_go.at[index, "REVENUE"] = int(row["UNIT_SALE_PRICE"] - row["UNIT_COST"])
        date_details : pd.DataFrame = convert_date(row["ORDER_DATE"])
        dates_go = pd.concat([dates_go, date_details], ignore_index=True)
    
    print("order_details done")
    return order_details_go[["ORDER_DETAIL_CODE", "PRODUCT_NUMBER", "QUANTITY", "UNIT_COST", "UNIT_PRICE", "UNIT_SALE_PRICE", "RETAILER_SITE_CODE", "ORDER_DATE", "ORDER_METHOD_EN", "SALES_STAFF_CODE", "REVENUE"]].rename(columns={
        "UNIT_SALE_PRICE" : "UNIT_SALES_PRICE"
    })

async def create_returned_items():
    print("returned_items started")
    await asyncio.sleep(1)
    global dates_go
    
    returned_items_go = pd.merge(sdm_frames["returned_item"], sdm_frames["return_reason"], left_on="RETURN_REASON_CODE", right_on="RETURN_REASON_CODE")
    returned_items_go = returned_items_go[["RETURN_CODE", "RETURN_DATE", "ORDER_DETAIL_CODE", "RETURN_DESCRIPTION_EN", "RETURN_QUANTITY"]]
    
    for index, row in returned_items_go.iterrows():
        date_details : pd.DataFrame = convert_date(row["RETURN_DATE"])
        returned_items_go.at[index, "RETURN_DATE"] = date_details["DATE"].iloc[0]
        dates_go = pd.concat([dates_go, date_details], ignore_index=True)
    
    print("returend_items done")
    return returned_items_go

    
async def main():
    print("main started")
    global forecast_go, inventory_go, sales_staff_go, retailer_site_go, product_go, order_details_go, returned_items_go, dates_go

    forecast_go, inventory_go, sales_staff_go, retailer_site_go, product_go, order_details_go, returned_items_go = await asyncio.gather(
        create_forecast(),
        create_inventory(),
        create_sales_staff(),
        create_retailer_site(),
        create_product(),
        create_order_details(),
        create_returned_items()
    )

    dates_go = dates_go.drop_duplicates()

    empty_go()

    tables = {
        "date": dates_go,
        "product": product_go,
        "product_forcast": forecast_go,
        "inventory": inventory_go,
        "sales_staff": sales_staff_go,
        "retailer_site": retailer_site_go,
        "order_details": order_details_go,
        "returned_item": returned_items_go
    }

    allowed = True

    for key in tables:
        for query in query_add(key, tables[key]):
            try:
                export_cursor_go.execute(query)
            except pyodbc.Error as e:
                print(query)
                print(e)
                allowed = False
                break

    if allowed:
        export_cursor_go.commit()
        print("ITEMS INSERTED")
    else:
        export_cursor_go.rollback()
        print("NOT ALLOWED TO COMMIT")