import os
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine,text
from openai import AzureOpenAI

# Load static STTM
def get_static_sttm():
    csv_text = """Source Column,Source Table,Target Column,Transformation
first_name,dim_customer,customer_name,concatenate first_name and last_name
last_name,dim_customer,customer_name,concatenate first_name and last_name
product_name,dim_product,product_name,lookup product_name from product_id
region,dim_customer,region,lookup region using customer_id
date,dim_date,sale_date,lookup date using date_id"""
    return pd.read_csv(StringIO(csv_text))

# Connect to MySQL and list tables
def get_db_tables():
    db_url = "mysql+pymysql://root:aman123@localhost:3306/reconciliation_db"
    engine = create_engine(db_url)
    with engine.connect() as conn:
        tables = pd.read_sql("SHOW TABLES", conn)
        return tables.values.flatten().tolist(), engine

# Fetch table data
def fetch_table_data(engine, table):
    return pd.read_sql(f"SELECT * FROM {table}", engine)

# Azure LLM client
def init_azure_client():
    return AzureOpenAI(
        api_key="",
        api_version="2024-02-01",
        azure_endpoint=""
    )

# Write output to file
def write_to_file(filename, content, domain):
    folder = f"Output_files/{domain}" if domain else "Output_files"
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ File written: {filepath}")

# Shared DB Engine
def get_db_engine():
    db_url = "mysql+pymysql://root:aman123@localhost:3306/reconciliation_db"
    return create_engine(db_url)

# Create backend table if not exists
def create_metadata_table():
    ddl = """
    CREATE TABLE IF NOT EXISTS reconciliation_metadata (
        id INT AUTO_INCREMENT PRIMARY KEY,
        domain VARCHAR(255),
        confluence_url TEXT,
        source_tables TEXT,
        target_table VARCHAR(255),
        generated_rules LONGTEXT,
        generated_sql LONGTEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    engine = get_db_engine()
    with engine.connect() as conn:
        conn.execute(text(ddl))
        conn.commit()

# Insert metadata
def insert_metadata(domain, confluence_url, source_tables, target_table, rules, sql):
    engine = get_db_engine()
    insert_sql = text("""
        INSERT INTO reconciliation_metadata
        (domain, confluence_url, source_tables, target_table, generated_rules, generated_sql)
        VALUES (:domain, :confluence_url, :source_tables, :target_table, :generated_rules, :generated_sql);
    """)
    with engine.connect() as conn:
        conn.execute(insert_sql, {
            "domain": domain,
            "confluence_url": confluence_url,
            "source_tables": ", ".join(source_tables),
            "target_table": target_table,
            "generated_rules": rules,
            "generated_sql": sql
        })
        conn.commit()    
