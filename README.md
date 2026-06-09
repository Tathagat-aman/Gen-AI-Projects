# Retail AI Analyst

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
- Data issues:
  - Re-generate `sales_data.csv` using `generate_sales_data()`
