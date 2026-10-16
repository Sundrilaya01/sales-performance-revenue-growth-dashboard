// Power Query (M) Ingestion Scripts for Power BI Desktop
// Project: Sales Performance & Revenue Growth Dashboard
// Place these expressions into Power Query Advanced Editor

// 1. Fact_Sales
let
    Source = Csv.Document(File.Contents("D:\Power BI\Sales Performance & Revenue Growth Dashboard\data\processed\fact_sales.csv"),[Delimiter=",", Columns=17, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"order_id", type text},
        {"date_key", Int64.Type},
        {"date", type date},
        {"product_id", type text},
        {"customer_id", type text},
        {"rep_id", type text},
        {"region_id", type text},
        {"units_sold", Int64.Type},
        {"unit_price", type number},
        {"sales_amount", type number},
        {"cost", type number},
        {"profit", type number},
        {"profit_margin_pct", type number},
        {"target_sales", type number},
        {"actual_sales", type number},
        {"achievement_pct", type number},
        {"growth_pct", type number}
    })
in
    #"Changed Type"

// 2. Dim_Products
let
    Source = Csv.Document(File.Contents("D:\Power BI\Sales Performance & Revenue Growth Dashboard\data\processed\dim_products.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"product_id", type text},
        {"product_name", type text},
        {"category", type text},
        {"unit_price", type number},
        {"unit_cost", type number},
        {"unit_margin", type number},
        {"target_margin_pct", type number}
    })
in
    #"Changed Type"

// 3. Dim_Customers
let
    Source = Csv.Document(File.Contents("D:\Power BI\Sales Performance & Revenue Growth Dashboard\data\processed\dim_customers.csv"),[Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"customer_id", type text},
        {"country", type text},
        {"region", type text},
        {"state_city", type text},
        {"customer_segment", type text},
        {"sales_channel", type text}
    })
in
    #"Changed Type"

// 4. Dim_Sales_Reps
let
    Source = Csv.Document(File.Contents("D:\Power BI\Sales Performance & Revenue Growth Dashboard\data\processed\dim_sales_reps.csv"),[Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"rep_id", type text},
        {"sales_rep_name", type text},
        {"assigned_region", type text}
    })
in
    #"Changed Type"

// 5. Dim_Regions
let
    Source = Csv.Document(File.Contents("D:\Power BI\Sales Performance & Revenue Growth Dashboard\data\processed\dim_regions.csv"),[Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"region_id", type text},
        {"region_name", type text},
        {"country", type text}
    })
in
    #"Changed Type"

// 6. Dim_Date
let
    Source = Csv.Document(File.Contents("D:\Power BI\Sales Performance & Revenue Growth Dashboard\data\processed\dim_date.csv"),[Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"date_key", Int64.Type},
        {"date", type date},
        {"year", Int64.Type},
        {"quarter", type text},
        {"quarter_name", type text},
        {"month_number", Int64.Type},
        {"month_name", type text},
        {"month_year", type text},
        {"day_of_month", Int64.Type},
        {"day_of_week", Int64.Type},
        {"day_name", type text},
        {"is_weekend", Int64.Type}
    })
in
    #"Changed Type"
