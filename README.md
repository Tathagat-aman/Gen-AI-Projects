# 1. Retail AI Analyst

A retail sales intelligence project that combines:
- A FastAPI backend powered by a LangGraph agent
- A Streamlit dashboard for metrics, charts, and chat
- Tool-based analytics for trend analysis, anomaly detection, and promo simulation
- Synthetic data generation for testing/demo

## Features

- Interactive dashboard with KPI cards and Plotly charts
- Dataset filtering by category and region
- Chat-based analytics assistant
- Built-in analytical tools:
  - `trend_tool`: sales trend and grouped comparisons
  - `anomaly_tool`: z-score anomaly detection
  - `simulation_tool`: promotion what-if simulation
- Synthetic retail data generator (`sales_data.csv`)

## Project Structure

- `streamlit_app.py` - Streamlit frontend dashboard and chat UI
- `api.py` - FastAPI service with health check and `/chat` endpoint
- `agent.py` - LangGraph workflow + LLM/tool binding
- `tool_functions.py` - Trend, anomaly, and simulation logic
- `synthetic_data.py` - Data generation and loading helpers
- `sales_data.csv` - Dataset used by dashboard and tools
- `requirements.txt` - Python dependencies

## Prerequisites

- Python 3.10+
- pip
- (Recommended) virtual environment
- Azure OpenAI deployment (used by `agent.py`)

## Installation

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Note: `agent.py` uses `dotenv` (`from dotenv import load_dotenv`) so you may need:

```bash
pip install python-dotenv
```

## Environment Variables

Create a `.env` file in this folder with your Azure OpenAI settings:

```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-08-01-preview
```

`agent.py` is configured with:
- `azure_deployment="gpt-4"`
- `api_version="2024-08-01-preview"`

Make sure your Azure deployment name matches the code.

## Run The App

Open two terminals in this folder.

1. Start the API:

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

2. Start the Streamlit UI:

```bash
streamlit run streamlit_app.py
```

Then open the Streamlit URL shown in terminal (usually `http://localhost:8501`).

## API Endpoints

- `GET /` - health check
- `POST /chat` - run the retail analyst agent

Example request:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Compare sales across regions"}]}'
```

## Example Prompts

- "Compare sales across regions"
- "Show anomalies in the Beverages category"
- "What if we run a 20% discount on Snacks?"
- "Which categories perform best on holidays?"

## Regenerate Synthetic Data

From Python:

```python
from synthetic_data import generate_sales_data
generate_sales_data(rows=100000, file_path="sales_data.csv")
```

Or use the **Regenerate Synthetic Data** button in the Streamlit sidebar.

## Troubleshooting

- API request failed from Streamlit:
  - Verify FastAPI is running at `http://localhost:8000`
- LLM errors:
  - Check `.env` values and Azure deployment name
- Module import errors:
  - Ensure venv is active and dependencies are installed
 







# 2. Data Reconciliation Agent

A GenAI-powered data reconciliation assistant that compares source and target tables, generates human-readable reconciliation rules, creates SQL reconciliation scripts, and stores generation metadata.

## What This Project Does

The application runs a multi-agent workflow:

1. Load selected source and target tables from MySQL.
2. Load STTM mapping (currently from a static in-code mapping).
3. Use Azure OpenAI to generate:
   - Reconciliation rules in English
   - SQL reconciliation script
4. Save generated outputs to files by domain.
5. Store metadata in a backend database table.

## Project Structure

- app.py: Streamlit UI entry point
- main.py: Agent orchestration pipeline
- agents.py: Agent class implementations
- tools.py: Database, LLM, STTM, and file utility functions
- sample_files/: Sample CSV files for reference/testing
- Output_files/: Generated output artifacts
- Data Reconciliation Agent/: Duplicate copy of the same app structure

## Tech Stack

- Python 3.10+
- Streamlit
- pandas
- SQLAlchemy
- PyMySQL
- OpenAI Python SDK (Azure OpenAI)
- MySQL

## Prerequisites

1. Python installed
2. MySQL running locally
3. Database created:
   - reconciliation_db
4. Source/target tables present in MySQL
5. Azure OpenAI endpoint and API key

## Installation

1. Open a terminal in the project root.
2. Create and activate a virtual environment.
3. Install dependencies:

pip install streamlit pandas sqlalchemy pymysql openai tabulate

## Configuration

Current code uses hardcoded placeholders/defaults in tools.py and app.py.

### MySQL Connection

Update the MySQL URL in:
- app.py
- tools.py (get_db_tables and get_db_engine)

Default currently used:
mysql+pymysql://root:aman123@localhost:3306/reconciliation_db

### Azure OpenAI

Update in tools.py -> init_azure_client:
- api_key
- azure_endpoint
- api_version (already set)

Model in use (agents.py):
- gpt-4o-mini-2024-07-18

## Run The App

From project root:

streamlit run app.py

Then open the local URL shown in terminal (usually http://localhost:8501).

## How To Use

1. Select one or more source tables.
2. Select a target table.
3. Enter business domain (example: Retail).
4. Enter requirement document URL (Confluence link field).
5. Click Generate Reconciliation Rules and SQL.

The UI displays:
- Generated rules
- Generated SQL
- Download buttons for both outputs

## Output Files

Generated files are written to:

Output_files/<domain>/

For example:
- Output_files/Retail/reconciliation_rules.txt
- Output_files/Retail/reconciliation_script.sql

## Metadata Table

The app creates/writes to this MySQL table:

reconciliation_metadata

Columns:
- id
- domain
- confluence_url
- source_tables
- target_table
- generated_rules
- generated_sql
- created_at

## Notes And Limitations

- STTM is currently static and loaded from a hardcoded CSV string in tools.py.
- Confluence URL is collected and stored, but not yet used to fetch STTM content.
- Database and Azure credentials are currently in source code placeholders/defaults.

## Suggested Next Improvements

1. Move MySQL and Azure settings to environment variables.
2. Add a requirements.txt file.
3. Add input validation/error handling for DB and LLM failures.
4. Replace static STTM with Confluence/API-based ingestion.
5. Add unit tests for tools and agents.

## License

No license file is currently included. Add a LICENSE file if you plan to publish or share this project.
- Data issues:
  - Re-generate `sales_data.csv` using `generate_sales_data()`
