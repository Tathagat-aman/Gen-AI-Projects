from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent import graph

app = FastAPI(title="Retail AI Analyst API")


class ChatRequest(BaseModel):
    messages: List[Dict[str, Any]]


class ChatResponse(BaseModel):
    assistant_message: Dict[str, Any]
    state: Dict[str, Any]


@app.get("/")
async def health_check() -> Dict[str, str]:
    return {"status": "ok", "message": "Retail AI Analyst API is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> Dict[str, Any]:
    try:
        state = graph.invoke({"messages": request.messages})
        assistant_message = state["messages"][-1]
        return {
            "assistant_message": {
                "content": assistant_message.content,
                "role": "assistant"
            },
            "state": state
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
