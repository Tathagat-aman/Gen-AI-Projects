import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from main import run_reconciliation
from tools import fetch_table_data

st.set_page_config(page_title="STTM-based Reconciliation Generator", layout="wide")
st.title("🔍 GenAI-Powered Reconciliation Config Generator")

# DB
db_url = "mysql+pymysql://root:aman123@localhost:3306/reconciliation_db"
engine = create_engine(db_url)

# UI: Select tables
with engine.connect() as conn:
    tables = pd.read_sql("SHOW TABLES", conn)
    table_list = tables.values.flatten().tolist()

source_selected = st.multiselect("Select Source Tables", options=table_list)
target_selected = st.selectbox("Select Target Table", options=table_list)
domain = st.text_input("Enter business domain:")
sttm_url = st.text_input("Enter Requirement Doc (Confluence URL):", placeholder="https://confluence/...")

# Trigger reconciliation
if st.button("🔄 Generate Reconciliation Rules and SQL"):
    if not (source_selected and target_selected and domain and sttm_url):
        st.error("Please fill in all fields including Confluence link.")
    else:
        rules, sql = run_reconciliation(
            source_tables=source_selected,
            target_table=target_selected,
            domain=domain,
            sttm_url=sttm_url,  
            st=st
        )

        st.subheader("✅ Reconciliation Rules")
        st.code(rules)

        st.subheader("💡 SQL Scripts")
        st.code(sql)

        st.download_button("⬇️ Download SQL Scripts", sql, file_name="reconciliation_script.sql")
        st.download_button("⬇️ Download Rules", rules, file_name="reconciliation_rules.txt")