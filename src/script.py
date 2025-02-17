from settings import settings, logger
import pandas as pd
import sqlite3 as sql

def run():
    goSalesTrainConn = sql.connect("../data/raw/go_sales_train.sqlite")

    products = pd.read_sql(f"SELECT * FROM product", goSalesTrainConn)
    product_types = pd.read_sql(f"SELECT * FROM product_type", goSalesTrainConn)
    product_lines = pd.read_sql(f"SELECT * FROM product_line", goSalesTrainConn)
    sales_staff = pd.read_sql(f"SELECT * FROM sales_staff", goSalesTrainConn)
    sales_branch = pd.read_sql(f"SELECT * FROM sales_branch", goSalesTrainConn)
    retailer_site = pd.read_sql(f"SELECT * FROM retailer_site", goSalesTrainConn)
    countries = pd.read_sql(f"SELECT * FROM country", goSalesTrainConn)
    order_headers = pd.read_sql(f"SELECT * FROM order_header", goSalesTrainConn)
    order_details = pd.read_sql(f"SELECT * FROM order_details", goSalesTrainConn)
    return_items = pd.read_sql(f"SELECT * FROM returned_item", goSalesTrainConn)
    return_reasons = pd.read_sql(f"SELECT * FROM return_reason", goSalesTrainConn)

    sql_query = "SELECT name FROM sqlite_master WHERE type='table';"

    pd.read_sql(sql_query, goSalesTrainConn)

    productionCostsInfo = products[(products["PRODUCTION_COST"] > 50) & (products["PRODUCTION_COST"] < 100)]
    productionCostsSpecific = productionCostsInfo[["PRODUCT_NAME", "PRODUCTION_COST"]]

    productionCostsSpecific

    prodctionMargeInfo = products[(products["MARGIN"] < 0.2) | (products["MARGIN"] > 0.6)]
    productionMargeSpecific = prodctionMargeInfo[["PRODUCT_NAME", "MARGIN"]]
    productionMargeSpecific

    countriesCurrencyInfo = countries[countries["CURRENCY_NAME"] == "francs"]
    countriesCurrencySpecific = countriesCurrencyInfo[["COUNTRY"]]

    countriesCurrencySpecific

    productIntroductionInfo = products[products["MARGIN"] > 0.5].drop_duplicates(subset=["INTRODUCTION_DATE"])
    productIntroductionInfo
    productIntroductionSpecific = productIntroductionInfo[["INTRODUCTION_DATE"]]

    productIntroductionSpecific

    sales_info = sales_branch[(sales_branch["ADDRESS2"].notna()) & (sales_branch["REGION"].notna())]
    sales_info[["ADDRESS1", "CITY"]]

    countriesCurrencyDollar = countries[(countries["CURRENCY_NAME"] == "dollars") | (countries["CURRENCY_NAME"] == "new dollar")]

    countriesCurrencyDollar = countriesCurrencyDollar.sort_values(by=["COUNTRY"])

    countriesCurrencyDollar

    retailsGermany = retailer_site[(retailer_site["POSTAL_ZONE"].astype(str).str[0] == "D") & (retailer_site["ADDRESS2"].notna())]
    retailsGermany = retailsGermany[["ADDRESS1", "ADDRESS2", "CITY"]]
    retailsGermany

    returendQuantity = pd.DataFrame({"RETUREND_QUANTITIES" : return_items[["RETURN_QUANTITY"]].sum()})

    returendQuantity
    totalRegions = pd.DataFrame({"Regions" : sales_branch[["REGION"]].drop_duplicates(subset=["REGION"]).count()})

    totalRegions
    
    lowest : float = products.nsmallest(1, "MARGIN")["MARGIN"].iloc[0]
    highest : float = products.nlargest(1, "MARGIN")["MARGIN"].iloc[0]
    allMargins : float = products["MARGIN"].sum()
    avarage : float = allMargins / products["MARGIN"].count()

    margeProductHighestLowest = pd.DataFrame({
        "LOWEST" : [lowest],
        "AVARGE" : [avarage],
        "HIGHEST" : [highest]
    })

    margeProductHighestLowest

    housingCustomer = retailer_site["ADDRESS2"].isna().sum()

    housingCustomerFrame = pd.DataFrame({"HOUSINGS" : [housingCustomer]})

    housingCustomerFrame

    avgCost = order_details.loc[(order_details["UNIT_SALE_PRICE"] < order_details["UNIT_PRICE"]), "UNIT_COST"].mean()

    avgCostFrame = pd.DataFrame({"AVG_COST" : [avgCost]})

    avgCostFrame

    sales_staff.groupby("POSITION_EN", as_index=False)["SALES_STAFF_CODE"].count()

    phones = sales_staff.groupby("WORK_PHONE", as_index=False)["SALES_STAFF_CODE"].count()

    phones = phones[phones["SALES_STAFF_CODE"] > 4]

    phones

    netherlands = pd.merge(retailer_site, countries, left_on="COUNTRY_CODE", how="inner", right_on="COUNTRY_CODE")

    netherlands = netherlands[(netherlands["COUNTRY_CODE"] == 7)]

    netherlands[["ADDRESS1", "CITY"]]

    eyewear = pd.merge(products, product_types, left_on="PRODUCT_TYPE_CODE", how="inner", right_on="PRODUCT_TYPE_CODE")

    eyewear = eyewear[eyewear["PRODUCT_TYPE_CODE"] == 11]
    eyewear[["PRODUCT_NAME"]]

    staff_order = pd.merge(sales_staff, order_headers, left_on="SALES_STAFF_CODE", how="inner", right_on="SALES_STAFF_CODE")
    retailer_staff = pd.merge(retailer_site, staff_order, left_on="RETAILER_SITE_CODE", how="inner", right_on="RETAILER_SITE_CODE")

    retailer_staff = retailer_staff[(retailer_staff["POSITION_EN"] == "Branch Manager")]

    retailer_staff[["FIRST_NAME", "LAST_NAME", "ADDRESS1"]].drop_duplicates()

    staff_sell = pd.merge(sales_staff, order_headers, left_on="SALES_STAFF_CODE", how="outer", right_on="SALES_STAFF_CODE")
    staff_sell = staff_sell[["POSITION_EN", "ORDER_DATE"]]
    staff_sell[staff_sell["POSITION_EN"].str.contains("Manager")].drop_duplicates()

    product_productType = pd.merge(products, product_types, left_on="PRODUCT_TYPE_CODE", how="inner", right_on="PRODUCT_TYPE_CODE")
    product_productType_orders = pd.merge(product_productType, order_details, left_on="PRODUCT_NUMBER", how="inner", right_on="PRODUCT_NUMBER")

    product_productType_orders = product_productType_orders[(product_productType_orders["QUANTITY"] > 750)]

    product_productType_orders = product_productType_orders[["PRODUCT_NAME", "PRODUCT_TYPE_EN"]]

    product_productType_orders.drop_duplicates()

    product_order = pd.merge(products, order_details, left_on="PRODUCT_NUMBER", how="inner", right_on="PRODUCT_NUMBER")

    product_order = product_order[((product_order["UNIT_PRICE"] - product_order["UNIT_SALE_PRICE"]) / product_order["UNIT_PRICE"]) > 0.4]

    product_order = product_order[["PRODUCT_NAME"]]

    product_order.drop_duplicates()

    returnItem_returnReason = pd.merge(return_items, return_reasons, left_on="RETURN_REASON_CODE", right_on="RETURN_REASON_CODE")
    returnItem_returnReason_order = pd.merge(returnItem_returnReason, order_details, left_on="ORDER_DETAIL_CODE", right_on="ORDER_DETAIL_CODE")

    returnItem_returnReason_order = returnItem_returnReason_order[((returnItem_returnReason_order["RETURN_QUANTITY"] / returnItem_returnReason_order["QUANTITY"]) > 0.9)]
    returnItem_returnReason_order = returnItem_returnReason_order[["RETURN_DESCRIPTION_EN"]]
    returnItem_returnReason_order.drop_duplicates()

    product_productType_numbers = product_productType.groupby("PRODUCT_TYPE_EN", as_index=False)["PRODUCT_NUMBER"].count().rename(columns={"PRODUCT_NUMBER" : "PRODUCT_COUNT"})

    product_productType_numbers
    country_retail = pd.merge(countries, retailer_site, left_on="COUNTRY_CODE", right_on="COUNTRY_CODE")
    country_retail = country_retail.groupby("COUNTRY", as_index=False)["RETAILER_CODE"].count()

    country_retail

    product_productType_ordersMerge = pd.merge(product_productType, order_details, left_on="PRODUCT_NUMBER", right_on="PRODUCT_NUMBER")

    cooking_gear = product_productType_ordersMerge[["PRODUCT_NAME", "QUANTITY", "UNIT_SALE_PRICE", "PRODUCT_TYPE_EN"]]
    cooking_gear = cooking_gear[(cooking_gear["PRODUCT_TYPE_EN"] == "Cooking Gear")]
    cooking_gear = cooking_gear.groupby(["PRODUCT_TYPE_EN", "PRODUCT_NAME"], as_index=False).agg({"QUANTITY" : "sum", "UNIT_SALE_PRICE" : 'mean'})
    cooking_gear = cooking_gear.rename(columns={"UNIT_SALE_PRICE" : "AVG_PRICE"})

    cooking_gear

    country_salesBranch = pd.merge(countries, sales_branch, left_on="COUNTRY_CODE", right_on="COUNTRY_CODE")
    country_salesBranch_retailer = pd.merge(country_salesBranch, retailer_site, left_on="COUNTRY_CODE", right_on="COUNTRY_CODE")

    country_salesBranch_retailer = country_salesBranch_retailer.groupby(["COUNTRY", "CITY_x"], as_index=False)["RETAILER_CODE"].count()
    country_salesBranch_retailer = country_salesBranch_retailer.rename(columns={
        "CITY_x" : "SALES_MAN",
        "RETAILER_CODE" : "CUSTOMER"
    })
    country_salesBranch_retailer
    
    staff_no_sales = []

    for index, row in sales_staff.iterrows():
        if row["SALES_STAFF_CODE"] not in order_headers["SALES_STAFF_CODE"].values:
            staff_no_sales.append(row)

    staff_no_sales = pd.DataFrame(staff_no_sales)

    staff_no_sales = staff_no_sales[["FIRST_NAME", "LAST_NAME"]]

    staff_no_sales
            
    less_then_average_margin = []
    avarage_margin = products["MARGIN"].mean()

    for index, row in products.iterrows():
        if row["MARGIN"] < avarage_margin:
            less_then_average_margin.append(row)

    less_then_average_margin = pd.DataFrame(less_then_average_margin)

    products_less_then_average_margin_total_average = less_then_average_margin[["MARGIN"]].mean()
    products_less_then_average_margin_total = less_then_average_margin[["MARGIN"]].count()

    overview_products_less_then_average = [
        int(products_less_then_average_margin_total),
        float(products_less_then_average_margin_total_average)
    ]

    overview_products_less_then_average = pd.DataFrame(overview_products_less_then_average)
    overview_products_less_then_average

    not_returned = pd.merge(products, order_details, left_on="PRODUCT_NUMBER", how="inner", right_on="PRODUCT_NUMBER")
    not_returned = pd.merge(not_returned, return_items, left_on="ORDER_DETAIL_CODE", how="inner", right_on="ORDER_DETAIL_CODE")

    not_returned = not_returned[not_returned["UNIT_SALE_PRICE"] > 500]
    not_returned = not_returned[["PRODUCT_NAME"]].drop_duplicates()
    not_returned
            
    manager = []

    for index, row in sales_staff.iterrows():
        if "Manager" in row["POSITION_EN"]:
            row["MANAGER"] = "Ja"
        else:
            row["MANAGER"] = "Nee"
        manager.append(row)

    manager = pd.DataFrame(manager)
    manager[["LAST_NAME", "MANAGER"]]
    
    from datetime import date
    date.today().year

    from datetime import datetime

    date_str = '16-8-2013'
    date_format = '%d-%m-%Y'
    date_obj = datetime.strptime(date_str, date_format)

    date_obj.year

    service = []

    date_format = "%Y-%m-%d"
    for index, row in sales_staff.iterrows():
        in_service = datetime.strptime(row["DATE_HIRED"], date_format).year
        today = date.today().year
        
        if (today - in_service) >= 12:
            row["12_YEAR"] = "lang in dienst"
        else:
            row["12_YEAR"] = "kort in dienst"
        
        if (in_service - today) < 25:
            row["25_YEAR"] = "kort in dienst"
        else:
            row["25_YEAR"] = "lang in dienst"
        
        service.append(row[["12_YEAR", "25_YEAR"]])

    service = pd.DataFrame(service)
    service
