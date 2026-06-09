from langchain_community.chat_models import ChatOllama
from langchain.tools import tool
from tool_functions import analyze_trend, detect_anomalies, simulate_promo

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import AzureChatOpenAI
llm = AzureChatOpenAI(
    azure_deployment="gpt-4",  # or your deployment
    api_version="2024-08-01-preview",  # or your api version
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)


@tool
def trend_tool(category: str = None, region: str = None, store_size: str = None, 
               holiday_flag: int = None, promo_flag: int = None, group_by: str = None) -> dict:
    """Analyzes sales trends with optional grouping.
    
    Parameters:
    - category: Filter by product category (Beverages, Snacks, Dairy, Personal Care, Household, Frozen Foods, Bakery)
    - region: Filter by store region (North, South, East, West)
    - store_size: Filter by store size (Small, Medium, Large)
    - holiday_flag: Filter by holiday (0=non-holiday, 1=holiday)
    - promo_flag: Filter by promotion (0=no promo, 1=promo)
    - group_by: Column to group results by. Valid values:
        * 'store_region' - Compare sales across regions
        * 'category' - Compare sales across product categories
        * 'store_size' - Compare sales across store sizes
        * 'holiday_flag' - Compare holiday vs non-holiday
        * 'promo_flag' - Compare promo vs non-promo
        * None - Show time-based trend with growth percentage
    
    Use for: comparisons, top performers, growth analysis, seasonal trends.
    Examples: "Compare regions", "Which categories sell best?", "Show sales by store size"
    """
    return analyze_trend(category=category, region=region, store_size=store_size,
                        holiday_flag=holiday_flag, promo_flag=promo_flag, group_by=group_by)


@tool
def anomaly_tool(category: str = None, region: str = None, store_size: str = None,
                 holiday_flag: int = None, promo_flag: int = None, threshold: float = 2.0) -> dict:
    """Detects unusual sales patterns using statistical analysis (z-score method).
    
    Parameters:
    - category: Focus on specific category (Beverages, Snacks, Dairy, Personal Care, Household, Frozen Foods, Bakery)
    - region: Focus on specific region (North, South, East, West)
    - store_size: Focus on specific store size (Small, Medium, Large)
    - holiday_flag: Focus on holidays (0=non-holiday, 1=holiday)
    - promo_flag: Focus on promotions (0=no promo, 1=promo)
    - threshold: Sensitivity (default 2.0 = moderate, higher = less sensitive)
    
    Returns daily anomalies with dates and z-scores.
    Use for: spikes, drops, outliers, unusual behavior.
    Examples: "Any unusual sales days?", "Show Beverages anomalies", "Detect spikes in North region"
    """
    return detect_anomalies(category=category, region=region, store_size=store_size,
                           holiday_flag=holiday_flag, promo_flag=promo_flag, threshold=threshold)


@tool
def simulation_tool(category: str, discount_pct: int, duration_days: int = 30,
                    region: str = None, store_size: str = None) -> dict:
    """Simulates promotional impact based on historical promo performance.
    
    Parameters:
    - category: REQUIRED - Product category to promote (Beverages, Snacks, Dairy, Personal Care, Household, Frozen Foods, Bakery)
    - discount_pct: REQUIRED - Discount percentage (e.g., 15 for 15% off)
    - duration_days: Promo duration in days (default 30)
    - region: Limit to specific region (North, South, East, West)
    - store_size: Limit to specific store size (Small, Medium, Large)
    
    Returns predicted units sold, revenue, and lift percentage.
    Use for: what-if analysis, ROI estimation, promo planning.
    Examples: "What if 20% discount on Snacks?", "Predict 15% off Beverages for 2 weeks"
    """
    return simulate_promo(category=category, discount_pct=discount_pct, duration_days=duration_days,
                         region=region, store_size=store_size)


tools = [trend_tool, anomaly_tool, simulation_tool]

llm_with_tools = llm.bind_tools(tools)


class State(TypedDict):
    messages: Annotated[List, add_messages]


def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages":[response]}


builder = StateGraph(State)

builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools","chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()