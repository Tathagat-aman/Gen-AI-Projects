from tools import get_static_sttm, get_db_tables, fetch_table_data, init_azure_client, write_to_file, create_metadata_table, insert_metadata

class DBAgent:
    def __init__(self):
        self.engine = None
        self.source_dfs = {}
        self.target_df = None

    def load_data(self, source_tables, target_table):
        tables, self.engine = get_db_tables()
        for table in source_tables:
            if table in tables:
                self.source_dfs[table] = fetch_table_data(self.engine, table)
        if target_table in tables:
            self.target_df = fetch_table_data(self.engine, target_table)
        else:
            raise ValueError("Target table not found.")

class STTMAgent:
    def __init__(self, confluence_url: str = ""):
        self.sttm_df = None
        self.confluence_url = confluence_url

    def load_sttm(self):
        print(f"ℹ️ Using STTM from Confluence URL: {self.confluence_url}")
        # TODO: Future logic to fetch from Confluence
        self.sttm_df = get_static_sttm()

class ReconAgent:
    def __init__(self):
        self.llm = init_azure_client()

    def generate_reconciliation(self, sttm_df, source_dfs, target_df, domain):
        ### Step 1: Generate English Rules
        rules_prompt = f"""
You are a data reconciliation expert.

Given the following:
- Business Domain: {domain}
- STTM Mapping Table:
{sttm_df.to_markdown(index=False)}

- Source Table Samples:
""" + "\n\n".join([f"{table}:\n{df.head(3).to_markdown(index=False)}" for table, df in source_dfs.items()]) + f"""

- Target Table Sample:
{target_df.head(3).to_markdown(index=False)}

Generate English Reconciliation Rules describing how to compare source and target data.
"""

        rules_response = self.llm.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": rules_prompt}],
        )
        rules_text = rules_response.choices[0].message.content.strip()

        #### Step 2: Generate SQL from rules + STTM
        sql_prompt = f"""
You have just generated the following English reconciliation rules:

{rules_text}

Now, using these rules, the STTM mapping, and the source/target table samples:

- STTM:
{sttm_df.to_markdown(index=False)}

- Source Tables:
""" + "\n\n".join([f"{table}:\n{df.head(3).to_markdown(index=False)}" for table, df in source_dfs.items()]) + f"""

- Target Table Sample:
{target_df.head(3).to_markdown(index=False)}

Write SQL code to perform this reconciliation accurately.
"""

        sql_response = self.llm.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": sql_prompt}],
        )
        sql_text = sql_response.choices[0].message.content.strip()

        return rules_text, sql_text

class WriterAgent:
    def write_outputs(self, rules, sql, domain):
        write_to_file("reconciliation_rules.txt", rules, domain)
        write_to_file("reconciliation_script.sql", sql, domain)

class DBWriterAgent:
    def __init__(self):
        pass

    def write_to_db(self, domain, confluence_url, source_tables, target_table, rules, sql):
        create_metadata_table()
        insert_metadata(
            domain=domain,
            confluence_url=confluence_url,
            source_tables=source_tables,
            target_table=target_table,
            rules=rules,
            sql=sql
        )