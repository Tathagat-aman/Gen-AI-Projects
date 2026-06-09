To perform the reconciliation based on the provided rules, source tables, target table, and transformation details, you can use SQL queries that join the source tables and the target table. Here’s the SQL code to validate each of the reconciliation rules described.

### SQL Code for Reconciliation

```sql
WITH sales_data AS (
    SELECT
        fs.sale_id,
        CONCAT(dc.first_name, ' ', dc.last_name) AS customer_name,
        dp.product_name,
        dc.region,
        dd.date AS sale_date,
        (fs.quantity * fs.price) AS revenue
    FROM
        fact_sales fs
    JOIN
        dim_customer dc ON fs.customer_id = dc.customer_id
    JOIN
        dim_product dp ON fs.product_id = dp.product_id
    JOIN
        dim_date dd ON fs.date_id = dd.date_id
)

SELECT
    t.sale_id AS target_sale_id,
    t.customer_name AS target_customer_name,
    sd.customer_name AS source_customer_name,
    t.product_name AS target_product_name,
    sd.product_name AS source_product_name,
    t.region AS target_region,
    sd.region AS source_region,
    t.sale_date AS target_sale_date,
    sd.sale_date AS source_sale_date,
    t.revenue AS target_revenue,
    sd.revenue AS source_revenue,
    CASE 
        WHEN t.customer_name = sd.customer_name THEN 1 ELSE 0 END AS customer_name_match,
    CASE 
        WHEN t.product_name = sd.product_name THEN 1 ELSE 0 END AS product_name_match,
    CASE 
        WHEN t.region = sd.region THEN 1 ELSE 0 END AS region_match,
    CASE 
        WHEN t.sale_date = sd.sale_date THEN 1 ELSE 0 END AS sale_date_match,
    CASE 
        WHEN t.revenue = sd.revenue THEN 1 ELSE 0 END AS revenue_match
FROM
    TargetTable t
LEFT JOIN
    sales_data sd ON t.sale_id = sd.sale_id;
```

### Explanation of the SQL Code
1. **With Clause (`sales_data`)**: This Common Table Expression (CTE) combines the necessary source data from the `fact_sales`, `dim_customer`, `dim_product`, and `dim_date` tables. It calculates the `customer_name`, `product_name`, `region`, `sale_date`, and calculated `revenue` based on the transformations defined in the mapping table.

2. **Main Select Statement**:
   - The `FROM TargetTable t` selects from the target table.
   - It performs a **LEFT JOIN** with the `sales_data` CTE based on `sale_id`.
   - Various comparisons are made between the target data and the derived source data, evaluating whether the customer name, product name, region, sale date, and revenue from both tables match.

3. **Case Statements**: Each CASE statement checks if the corresponding columns from the target and source data match, returning either 1 (match) or 0 (not a match).

### Conclusion
This SQL query provides a detailed comparison between the target and expected source data according to the transformation rules. You can review the output for discrepancies to ensure data quality and consistency in your reconciliation process. Adjust the `TargetTable` name with the actual name of your target table in your database when executing the SQL.