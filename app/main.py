import logging

from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from app.services.order_service import (
    get_orders, get_total_revenue, get_montly_revenue, get_monthly_profit, get_monthly_revenue_pandas
)

from app.services.marketing_service import (
    get_marketing_campaigns, get_channel_performance
)

from app.services.gemini_service import (
    classify_question,
    execute_operation
)

from app.services.target_service import get_monthly_targets

from app.data_agents.data_agent import DataAgent

from app.knowledge_agents.knowledge_agent import KnowledgeAgent

from app.action_agents.action_agent import ActionAgent

from app.orchestrator.graph import aegis_graph

from app.orchestrator.graph import aegis_graph

from app.startup import initialize_knowledge

knowledge_agent = KnowledgeAgent()
action_agent = ActionAgent()

app = FastAPI(title = "Aegis Mini API")
initialize_knowledge()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_agent = DataAgent()


class ChatRequest (BaseModel):
    question:str

class ActionRequest(BaseModel):
    action: str
    approved: bool = False

@app.get("/")
def home():
    return {
        "message": "Aegis is running"
    }

@app.post("/api/v1/chat")
def chat(request: ChatRequest):
    logger.info(
        "Chat request received: %s",
        request.question
    )

    result = aegis_graph.invoke({
        "question": request.question
    })

    logger.info(
        "Request routed to: %s",
        result.get("route")
    )

    return {
        "question": request.question,
        "route": result.get("route"),
        "result": result.get("result"),
    }
# @app.post("/api/v1/chat")
# def chat(request: ChatRequest):

#     operation = classify_question(request.question)

#     result = execute_operation(operation)

#     return {
#         "question": request.question,
#         "operation": operation.operation,
#         "result": result
#     }

@app.post("/api/v1/chat")
def chat(request: ChatRequest):
    result = aegis_graph.invoke({
        "question": request.question
    })

    return {
        "question": request.question,
        "route": result.get("route"),
        "result": result.get("result"),
    }

@app.get("/api/v1/orders")
def orders():
    return{
        "orders": get_orders()
    }

@app.get("/api/v1/analytics/revenue")
def total_revenue():
    return {
        "total_revenue": get_total_revenue()
    }

@app.get("/api/v1/analytics/monthly-revenue")
def monthly_revenue():
    return {
        "monthly_revenue": get_montly_revenue()
    }

@app.get("/api/v1/analytics/monthly-profit")
def monthly_profit():
    return {
        "monthly_profit": get_monthly_profit()
    }

@app.get("/api/v1/analytics/monthly-revenue-pandas")
def monthly_revenue_pandas():
    return {
        "monthly_revenue": get_monthly_revenue_pandas()
    }

@app.get("/api/v1/marketing/campaigns")
def marketing_campaigns():
    return{
        "campaign": get_marketing_campaigns()
    }

@app.get("/api/v1/marketing/channel-performance")
def channel_performance():
    return{
        "channel_performance": get_channel_performance()
    }

@app.get("/api/v1/targets/monthly")
def monthly_targets():
    return {
        "monthly_targets": get_monthly_targets()
    }

data_agent = DataAgent()


@app.get("/api/v1/data/revenue")
def data_revenue():
    return {
        "total_revenue": data_agent.total_revenue()
    }


@app.get("/api/v1/data/monthly-revenue")
def data_monthly_revenue():
    return {
        "monthly_revenue": data_agent.monthly_revenue()
    }


@app.get("/api/v1/data/monthly-profit")
def data_monthly_profit():
    return {
        "monthly_profit": data_agent.monthly_profit()
    }

@app.post("/api/v1/knowledge")
def knowledge(request: ChatRequest):

    result = knowledge_agent.answer_question(
        request.question
    )

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }

    
@app.post("/api/v1/actions")
def execute_action(request: ActionRequest):

    result = action_agent.execute(
        action_name=request.action,
        approved=request.approved
    )

    return result

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "aegis-api"
    }

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("aegis")