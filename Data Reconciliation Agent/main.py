from agents import DBAgent, STTMAgent, ReconAgent, WriterAgent, DBWriterAgent
import time

def run_reconciliation(source_tables, target_table, domain, sttm_url, st):
    # AGENT 1: DBAgent - Load source and target tables from database
    st.markdown("### 🧠 Agent 1: `DBAgent` - Source and Target Table Loader")
    time.sleep(1)  # Simulate processing time
    st.info("🚀 Starting Agent 1 task: Loading selected tables from database...")
    time.sleep(1)  # Simulate processing time
    st.markdown("🛠️ Tool Invoked: `SQLAlchemy + pandas.read_sql()`")
    db_agent = DBAgent()
    db_agent.load_data(source_tables, target_table)
    time.sleep(1)  # Simulate processing time
    st.success("✅ Agent 1 task complete: Tables loaded successfully.")

    time.sleep(3)  # Simulate processing time

    # AGENT 2: STTMAgent - Load STTM from static source (Confluence URL will be used in future)
    st.markdown("### 📄 Agent 2: `STTMAgent` - STTM Mapper Loader")
    time.sleep(1)  # Simulate processing tim
    st.info("🚀 Starting Agent 2 task: Loading STTM from static source (Confluence URL will be used in future).")
    time.sleep(1)  # Simulate processing time
    st.markdown(f"🔗 Requirement Doc (Confluence URL): `{sttm_url}`")
    st.markdown("🛠️ Tool Invoked: `get_static_sttm()`")
    time.sleep(1)  # Simulate processing time
    sttm_agent = STTMAgent(confluence_url=sttm_url)
    sttm_agent.load_sttm()
    time.sleep(1)  # Simulate processing time
    st.success("✅ Agent 2 task complete: STTM mapping loaded.")

    time.sleep(3)  # Simulate processing time

    # AGENT 3: ReconAgent - Generate reconciliation rules and SQL
    st.markdown("### 🤖 Agent 3: `ReconAgent` - Rule and SQL Generator")
    time.sleep(1)  # Simulate processing time
    st.info("🚀 Starting Agent 3 task: Generating reconciliation rules and SQL.")
    time.sleep(1)  # Simulate processing time
    st.markdown("🛠️ Tool Invoked: `Azure OpenAI - GPT-4o-mini`")
    recon_agent = ReconAgent()
    rules, sql = recon_agent.generate_reconciliation(
        sttm_df=sttm_agent.sttm_df,
        source_dfs=db_agent.source_dfs,
        target_df=db_agent.target_df,
        domain=domain
    )
    st.success("✅ Agent 3 task complete: Reconciliation rules and SQL generated.")

    time.sleep(3)  # Simulate processing time

    # Agent 4: WriterAgent
    st.markdown("### 💾 Agent 4: `WriterAgent` - File Writer")
    time.sleep(1)  # Simulate processing time
    st.info("🚀 Starting Agent 4 task: Writing output files to disk...")
    time.sleep(1)  # Simulate processing time
    st.markdown("🛠️ Tool Invoked: `write_to_file()`")
    writer = WriterAgent()
    writer.write_outputs(rules, sql, domain)
    time.sleep(1)  # Simulate processing time
    st.success("✅ Agent 4 task complete: Rules and SQL written to `Output_files/`.")

    time.sleep(3)  # Simulate processing time


    # Agent 5: DBWriterAgent
    st.markdown("### 🗃️ Agent 5: `DBWriterAgent` - Store Reconciliation Metadata in Backend DB")
    time.sleep(1)  # Simulate processing time
    st.info("🚀 Starting Agent 5 task: Inserting outputs into `reconciliation_metadata` table...")
    time.sleep(1)  # Simulate processing time
    st.markdown("🛠️ Tool Invoked: `create_metadata_table()` + `insert_metadata()` (via SQLAlchemy)")

    db_writer = DBWriterAgent()
    db_writer.write_to_db(
        domain=domain,
        confluence_url=sttm_url,
        source_tables=source_tables,
        target_table=target_table,
        rules=rules,
        sql=sql
    )

    st.success("✅ Agent 5 task complete: Metadata saved in MySQL database.")

    time.sleep(3)  # Simulate processing time
    st.markdown("---")
    st.markdown("🎉 **All agents completed their tasks successfully!**")
    return rules, sql
