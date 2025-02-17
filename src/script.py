from settings import settings, logger

def run():
    # %% [markdown]
    # # Werkcollege-opdrachten Week 1.3

    # %% [markdown]
    # ## Dependencies importeren

    # %% [markdown]
    # Kopieer in het codeblok hieronder van het vorige practicum de import-code voor de dependencies die het vaakst worden gebruikt om data in te lezen. Geef er ook de gebruikelijke aliassen aan.<br>
    # Zet eventuele warnings uit.

    # %%
    import pandas as pd
    import sqlite3 as sql

    # %% [markdown]
    # Zet het bestand go_sales_train.sqlite in een makkelijk te vinden map

    # %% [markdown]
    # ## Databasetabellen inlezen

    # %% [markdown]
    # Kopieer in het codeblok hieronder van het vorige practicum de code om een connectie met het bestand go_sales_train.sqlite te maken.

    # %%
    goSalesTrainConn = sql.connect("../data/raw/go_sales_train.sqlite")

    # %% [markdown]
    # Lees van de ingelezen go_sales_train-database te volgende tabellen in met behulp van "SELECT * FROM *tabel*".
    # - product
    # - product_type
    # - product_line
    # - sales_staff
    # - sales_branch
    # - retailer_site
    # - country
    # - order_header
    # - order_details
    # - returned_item
    # - return_reason

    # %%
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

    # %% [markdown]
    # Krijg je een "no such table" error? Dan heb je misschien met .connect() per ongeluk een leeg  databasebestand (.sqlite) aangemaakt. <u>Let op:</u> lees eventueel de informatie uit het Notebook van werkcollege 1.1b nog eens goed door.

    # %% [markdown]
    # Als je tijdens onderstaande opdrachten uit het oog verliest welke tabellen er allemaal zijn, kan je deze Pythoncode uitvoeren:

    # %%
    sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
    #Vul dit codeblok verder in
    #pd.read_sql(sql_query, ...)
    pd.read_sql(sql_query, goSalesTrainConn)
    #Op de puntjes hoort de connectie naar go_sales_train óf go_staff_train óf go_crm_train te staan.

    # %% [markdown]
    # erachter 

    # %% [markdown]
    # Let op! Voor alle onderstaande opdrachten mag je <u>alleen Python</u> gebruiken, <u>geen SQL!</u>

    # %% [markdown]
    # ## Selecties op één tabel zonder functies

    # %% [markdown]
    # Geef een overzicht met daarin de producten en hun productiekosten waarvan de productiekosten lager dan 100 dollar en hoger dan 50 dollar ligt. (2 kolommen, 23 rijen)

    # %%
    productionCostsInfo = products[(products["PRODUCTION_COST"] > 50) & (products["PRODUCTION_COST"] < 100)]
    productionCostsSpecific = productionCostsInfo[["PRODUCT_NAME", "PRODUCTION_COST"]]

    productionCostsSpecific

    # %% [markdown]
    # Geef een overzicht met daarin de producten en hun marge waarvan de marge lager dan 20 % of hoger dan 60 % ligt. (2 kolommen, 7 rijen) 

    # %%
    prodctionMargeInfo = products[(products["MARGIN"] < 0.2) | (products["MARGIN"] > 0.6)]
    productionMargeSpecific = prodctionMargeInfo[["PRODUCT_NAME", "MARGIN"]]
    productionMargeSpecific

    # %% [markdown]
    # Geef een overzicht met daarin de landen waar met francs wordt betaald. Sorteer de uitkomst op land.  (1 kolom, 3 rijen)

    # %%
    countriesCurrencyInfo = countries[countries["CURRENCY_NAME"] == "francs"]
    countriesCurrencySpecific = countriesCurrencyInfo[["COUNTRY"]]

    countriesCurrencySpecific


    # %% [markdown]
    # Geef een overzicht met daarin de verschillende introductiedatums waarop producten met meer dan 50% marge worden geïntroduceerd (1 kolom, 7 rijen) 

    # %%
    productIntroductionInfo = products[products["MARGIN"] > 0.5].drop_duplicates(subset=["INTRODUCTION_DATE"])
    productIntroductionInfo
    productIntroductionSpecific = productIntroductionInfo[["INTRODUCTION_DATE"]]

    productIntroductionSpecific

    # %% [markdown]
    # Geef een overzicht met daarin het eerste adres en de stad van verkoopafdelingen waarvan zowel het tweede adres als de regio bekend is (2 kolommen, 7 rijen)

    # %%
    sales_info = sales_branch[(sales_branch["ADDRESS2"].notna()) & (sales_branch["REGION"].notna())]
    sales_info[["ADDRESS1", "CITY"]]

    # %% [markdown]
    # Geef een overzicht met daarin de landen waar met dollars (dollars of new dollar) wordt betaald. Sorteer de uitkomst op land. (1 kolom, 4 rijen) 

    # %%
    countriesCurrencyDollar = countries[(countries["CURRENCY_NAME"] == "dollars") | (countries["CURRENCY_NAME"] == "new dollar")]

    countriesCurrencyDollar = countriesCurrencyDollar.sort_values(by=["COUNTRY"])

    countriesCurrencyDollar

    # %% [markdown]
    # Geef een overzicht met daarin beide adressen en de stad van vestigingen van klanten waarvan de postcode begint met een ‘D’ (van duitsland). Filter op vestigingen die een tweede adres hebben. (3 kolommen, 2 rijen) 

    # %%
    retailsGermany = retailer_site[(retailer_site["POSTAL_ZONE"].astype(str).str[0] == "D") & (retailer_site["ADDRESS2"].notna())]
    retailsGermany = retailsGermany[["ADDRESS1", "ADDRESS2", "CITY"]]
    retailsGermany

    # %% [markdown]
    # ## Selecties op één tabel met functies

    # %% [markdown]
    # Geef het totaal aantal producten dat is teruggebracht (1 waarde) 

    # %%
    returendQuantity = pd.DataFrame({"RETUREND_QUANTITIES" : return_items[["RETURN_QUANTITY"]].sum()})

    returendQuantity

    # %% [markdown]
    # Geef het aantal regio’s waarin verkoopafdelingen gevestigd zijn. (1 waarde)

    # %%
    totalRegions = pd.DataFrame({"Regions" : sales_branch[["REGION"]].drop_duplicates(subset=["REGION"]).count()})

    totalRegions

    # %% [markdown]
    # Maak 3 variabelen:
    # - Een met de laagste
    # - Een met de hoogste
    # - Een met de gemiddelde (afgerond op 2 decimalen)
    # 
    # marge van producten (3 kolommen, 1 rij) 

    # %%
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

    # %% [markdown]
    # Geef het aantal vestigingen van klanten waarvan het 2e adres niet bekend is (1 waarde)

    # %%
    housingCustomer = retailer_site["ADDRESS2"].isna().sum()

    housingCustomerFrame = pd.DataFrame({"HOUSINGS" : [housingCustomer]})

    housingCustomerFrame

    # %% [markdown]
    # Geef de gemiddelde kostprijs van de verkochte producten waarop korting (unit_sale_price < unit_price) is verleend (1 waarde) 

    # %%
    avgCost = order_details.loc[(order_details["UNIT_SALE_PRICE"] < order_details["UNIT_PRICE"]), "UNIT_COST"].mean()

    avgCostFrame = pd.DataFrame({"AVG_COST" : [avgCost]})

    avgCostFrame

    # %% [markdown]
    # Geef een overzicht met daarin het aantal medewerkers per medewerkersfunctie (2 kolommen, 7 rijen) 

    # %%
    sales_staff.groupby("POSITION_EN", as_index=False)["SALES_STAFF_CODE"].count()


    # %% [markdown]
    # Geef een overzicht met daarin per telefoonnummer het aantal medewerkers dat op dat telefoonnummer bereikbaar is. Toon alleen de telefoonnummer waarop meer dan 4 medewerkers bereikbaar zijn. (2 kolommen, 10 rijen) 

    # %%
    phones = sales_staff.groupby("WORK_PHONE", as_index=False)["SALES_STAFF_CODE"].count()

    phones = phones[phones["SALES_STAFF_CODE"] > 4]

    phones

    # %% [markdown]
    # ## Selecties op meerdere tabellen zonder functies

    # %% [markdown]
    # Geef een overzicht met daarin het eerste adres en de stad van vestigingen van klanten uit ‘Netherlands’ (2 kolommen, 20 rijen) 

    # %%
    netherlands = pd.merge(retailer_site, countries, left_on="COUNTRY_CODE", how="inner", right_on="COUNTRY_CODE")

    netherlands = netherlands[(netherlands["COUNTRY_CODE"] == 7)]

    netherlands[["ADDRESS1", "CITY"]]

    # %% [markdown]
    # Geef een overzicht met daarin de productnamen die tot het producttype ‘Eyewear’ behoren. (1 kolom, 5 rijen) 

    # %%
    eyewear = pd.merge(products, product_types, left_on="PRODUCT_TYPE_CODE", how="inner", right_on="PRODUCT_TYPE_CODE")

    eyewear = eyewear[eyewear["PRODUCT_TYPE_CODE"] == 11]
    eyewear[["PRODUCT_NAME"]]

    # %% [markdown]
    # Geef een overzicht met daarin alle unieke eerste adressen van klantvestigingen en de voornaam en achternaam van de verkopers die ‘Branch Manager’ zijn en aan deze vestigingen hebben verkocht (3 kolommen, 1 rij) 

    # %%
    staff_order = pd.merge(sales_staff, order_headers, left_on="SALES_STAFF_CODE", how="inner", right_on="SALES_STAFF_CODE")
    retailer_staff = pd.merge(retailer_site, staff_order, left_on="RETAILER_SITE_CODE", how="inner", right_on="RETAILER_SITE_CODE")

    retailer_staff = retailer_staff[(retailer_staff["POSITION_EN"] == "Branch Manager")]

    retailer_staff[["FIRST_NAME", "LAST_NAME", "ADDRESS1"]].drop_duplicates()

    # %% [markdown]
    # Geef een overzicht met daarin van de verkopers hun functie en indien zij iets hebben verkocht de datum waarop de verkoop heeft plaatsgevonden. Laat alleen de verschillende namen van de posities zien van de verkopers die het woord ‘Manager’ in hun positienaam hebben staan. (2 kolommen, 7 rijen) 

    # %%
    staff_sell = pd.merge(sales_staff, order_headers, left_on="SALES_STAFF_CODE", how="outer", right_on="SALES_STAFF_CODE")
    staff_sell = staff_sell[["POSITION_EN", "ORDER_DATE"]]
    staff_sell[staff_sell["POSITION_EN"].str.contains("Manager")].drop_duplicates()

    # %% [markdown]
    # Geef een overzicht met daarin de verschillende namen van producten en bijbehorende namen van producttypen van de producten waarvoor ooit meer dan 750 stuks tegelijk verkocht zijn. (2 kolommen, 9 rijen) 

    # %%
    product_productType = pd.merge(products, product_types, left_on="PRODUCT_TYPE_CODE", how="inner", right_on="PRODUCT_TYPE_CODE")
    product_productType_orders = pd.merge(product_productType, order_details, left_on="PRODUCT_NUMBER", how="inner", right_on="PRODUCT_NUMBER")

    product_productType_orders = product_productType_orders[(product_productType_orders["QUANTITY"] > 750)]

    product_productType_orders = product_productType_orders[["PRODUCT_NAME", "PRODUCT_TYPE_EN"]]

    product_productType_orders.drop_duplicates()

    # %% [markdown]
    # Geef een overzicht met daarin de productnamen waarvan ooit meer dan 40% korting is verleend. De formule voor korting is: (unit_price - unit_sale_price) / unit_price (1 kolom, 8 rijen) 

    # %%
    product_order = pd.merge(products, order_details, left_on="PRODUCT_NUMBER", how="inner", right_on="PRODUCT_NUMBER")

    product_order = product_order[((product_order["UNIT_PRICE"] - product_order["UNIT_SALE_PRICE"]) / product_order["UNIT_PRICE"]) > 0.4]

    product_order = product_order[["PRODUCT_NAME"]]

    product_order.drop_duplicates()

    # %% [markdown]
    # Geef een overzicht met daarin de retourreden van producten waarvan ooit meer dan 90% van de aangeschafte hoeveelheid is teruggebracht (return_quantity/quantity). (1 kolom, 3 rijen) 

    # %%
    returnItem_returnReason = pd.merge(return_items, return_reasons, left_on="RETURN_REASON_CODE", right_on="RETURN_REASON_CODE")
    returnItem_returnReason_order = pd.merge(returnItem_returnReason, order_details, left_on="ORDER_DETAIL_CODE", right_on="ORDER_DETAIL_CODE")

    returnItem_returnReason_order = returnItem_returnReason_order[((returnItem_returnReason_order["RETURN_QUANTITY"] / returnItem_returnReason_order["QUANTITY"]) > 0.9)]
    returnItem_returnReason_order = returnItem_returnReason_order[["RETURN_DESCRIPTION_EN"]]
    returnItem_returnReason_order.drop_duplicates()

    # %% [markdown]
    # ## Selecties op meerdere tabellen met functies

    # %% [markdown]
    # Geef een overzicht met daarin per producttype het aantal producten die tot dat producttype behoren. (2 kolommen, 21 rijen) 

    # %%
    product_productType_numbers = product_productType.groupby("PRODUCT_TYPE_EN", as_index=False)["PRODUCT_NUMBER"].count().rename(columns={"PRODUCT_NUMBER" : "PRODUCT_COUNT"})

    product_productType_numbers

    # %% [markdown]
    # Geef een overzicht met daarin per land het aantal vestigingen van klanten die zich in dat land bevinden. (2 kolommen, 21 rijen) 

    # %%
    country_retail = pd.merge(countries, retailer_site, left_on="COUNTRY_CODE", right_on="COUNTRY_CODE")
    country_retail = country_retail.groupby("COUNTRY", as_index=False)["RETAILER_CODE"].count()

    country_retail

    # %% [markdown]
    # Geef een overzicht met daarin van de producten behorend tot het producttype ‘Cooking Gear’ per productnaam de totaal verkochte hoeveelheid en de gemiddelde verkoopprijs. Sorteer de uitkomst op totaal verkochte hoeveelheid. (4 kolommen, 10 rijen) 

    # %%
    product_productType_ordersMerge = pd.merge(product_productType, order_details, left_on="PRODUCT_NUMBER", right_on="PRODUCT_NUMBER")

    cooking_gear = product_productType_ordersMerge[["PRODUCT_NAME", "QUANTITY", "UNIT_SALE_PRICE", "PRODUCT_TYPE_EN"]]
    cooking_gear = cooking_gear[(cooking_gear["PRODUCT_TYPE_EN"] == "Cooking Gear")]
    cooking_gear = cooking_gear.groupby(["PRODUCT_TYPE_EN", "PRODUCT_NAME"], as_index=False).agg({"QUANTITY" : "sum", "UNIT_SALE_PRICE" : 'mean'})
    cooking_gear = cooking_gear.rename(columns={"UNIT_SALE_PRICE" : "AVG_PRICE"})

    cooking_gear

    # %% [markdown]
    # Geef een overzicht met daarin per land de naam van het land, de naam van de stad waar de verkoopafdeling is gevestigd (noem de kolomnaam in het overzicht ‘verkoper’) en het aantal steden waar zich klanten bevinden in dat land (noem de kolomnaam in het overzicht ‘klanten’) (3 kolommen, 29 rijen) 

    # %%
    country_salesBranch = pd.merge(countries, sales_branch, left_on="COUNTRY_CODE", right_on="COUNTRY_CODE")
    country_salesBranch_retailer = pd.merge(country_salesBranch, retailer_site, left_on="COUNTRY_CODE", right_on="COUNTRY_CODE")

    country_salesBranch_retailer = country_salesBranch_retailer.groupby(["COUNTRY", "CITY_x"], as_index=False)["RETAILER_CODE"].count()
    country_salesBranch_retailer = country_salesBranch_retailer.rename(columns={
        "CITY_x" : "SALES_MAN",
        "RETAILER_CODE" : "CUSTOMER"
    })
    country_salesBranch_retailer

    # %% [markdown]
    # ## Pythonvertalingen van SUBSELECT en UNION met o.a. for-loops

    # %% [markdown]
    # Geef een overzicht met daarin de voornaam en de achternaam van de medewerkers die nog nooit wat hebben verkocht (2 kolommen, 25 rijen) 

    # %%
    staff_no_sales = []

    for index, row in sales_staff.iterrows():
        if row["SALES_STAFF_CODE"] not in order_headers["SALES_STAFF_CODE"].values:
            staff_no_sales.append(row)

    staff_no_sales = pd.DataFrame(staff_no_sales)

    staff_no_sales = staff_no_sales[["FIRST_NAME", "LAST_NAME"]]

    staff_no_sales
            

    # %% [markdown]
    # Geef een overzicht met daarin het aantal producten waarvan de marge lager is dan de gemiddelde marge van alle producten samen. Geef in het overzicht tevens aan wat de gemiddelde marge is van dit aantal producten waarvan de marge lager dan de gemiddelde marge van alle producten samen is. (1 kolom, 2 rijen) 

    # %%
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


    # %% [markdown]
    # Geef een overzicht met daarin de namen van de producten die voor meer dan 500 (verkoopprijs) zijn verkocht maar nooit zijn teruggebracht. (1 kolom, 13 rijen) 

    # %%
    not_returned = pd.merge(products, order_details, left_on="PRODUCT_NUMBER", how="inner", right_on="PRODUCT_NUMBER")
    not_returned = pd.merge(not_returned, return_items, left_on="ORDER_DETAIL_CODE", how="inner", right_on="ORDER_DETAIL_CODE")

    not_returned = not_returned[not_returned["UNIT_SALE_PRICE"] > 500]
    not_returned = not_returned[["PRODUCT_NAME"]].drop_duplicates()
    not_returned
            

    # %% [markdown]
    # Geef een overzicht met daarin per (achternaam van) medewerker of hij/zij manager is of niet, door deze informatie toe te voegen als extra 'Ja/Nee'-kolom.<br>
    # Hint: gebruik een for-loop waarin je o.a. bepaalt of het woord 'Manager' in de functie (position_en) staat. (2 kolommen, 102 rijen).

    # %%
    manager = []

    for index, row in sales_staff.iterrows():
        if "Manager" in row["POSITION_EN"]:
            row["MANAGER"] = "Ja"
        else:
            row["MANAGER"] = "Nee"
        manager.append(row)

    manager = pd.DataFrame(manager)
    manager[["LAST_NAME", "MANAGER"]]

    # %% [markdown]
    # Met de onderstaande code laat je Python het huidige jaar uitrekenen.

    # %%
    from datetime import date
    date.today().year

    # %% [markdown]
    # Met de onderstaande code selecteer je op een bepaald jaartal uit een datum.

    # %%
    from datetime import datetime

    date_str = '16-8-2013'
    date_format = '%d-%m-%Y'
    date_obj = datetime.strptime(date_str, date_format)

    date_obj.year

    # %% [markdown]
    # Geef met behulp van bovenstaande hulpcode een overzicht met daarin op basis van het aantal jaar dat iemand in dienst is of een medewerker ‘kort in dienst’ (minder dan 25 jaar in dienst) of een ‘lang in dienst’ (groter gelijk dan 12 jaar in dienst) is. Geef daarbij per medewerker in een aparte kolom zowel ‘kort in dienst’ als ‘lang in dienst’ aan. Gebruik (wederom) een for-loop.<br>
    # (2 kolommen, 102 rijen) 

    # %%
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

    # %% [markdown]
    # ## Van Jupyter Notebook naar Pythonproject

    # %% [markdown]
    # 1. Richt de map waarin jullie tot nu toe hebben gewerkt in volgens de mappenstructuur uit de slides.
    # 2. Maak van de ontstane mappenstructuur een Pythonproject dat uitvoerbaar is vanuit de terminal. Maak daarin een .py-bestand dat minstens 5 antwoorden uit dit notebook (in de vorm van een DataFrame) exporteert naar Excelbestanden. Alle notebooks mogen als notebook blijven bestaan.
    # 3. Zorg ervoor dat dit Pythonproject zijn eigen repo heeft op Github. Let op: je virtual environment moet <b><u>niet</u></b> meegaan naar Github.
    # 
    # Je mag tijdens dit proces je uit stap 1 ontstane mappenstructuur aanpassen, zolang je bij het beoordelingsmoment kan verantwoorden wat de motivatie hierachter is. De slides verplichten je dus nergens toe.
    
    logger.log()

