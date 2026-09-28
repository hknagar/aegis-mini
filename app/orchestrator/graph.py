from langgraph.graph import StateGraph, START, END

from app.orchestrator.state import AegisState

from app.services.gemini_service import classify_route

from app.data_agents.data_agent import DataAgent

from app.knowledge_agents.knowledge_agent import KnowledgeAgent

data_agent = DataAgent()

knowledge_agent = KnowledgeAgent()


def classify_node(state: AegisState):

    result = classify_route(
        state["question"]
    )

    return {
        "route": result.route
    }

# from app.orchestrator.state import AegisState


# def classify_node(state: AegisState):

#     question = state["question"].lower()

#     if any(
#         word in question
#         for word in [
#             "refund",
#             "policy",
#             "shipping",
#             "support"
#         ]
#     ):
#         route = "knowledge"

#     else:
#         route = "data"

#     return {
#         "route": route
#     }

def data_node(state: AegisState):

    question = state["question"].lower()

    if "monthly profit" in question:
        result = data_agent.monthly_profit()

    elif "monthly revenue" in question:
        result = data_agent.monthly_revenue()

    elif "total revenue" in question or "revenue" in question:
        result = data_agent.total_revenue()

    else:
        result = {
            "message": "I don't know which data operation to perform."
        }

    return {
        "result": result
    }

# def data_node(state: AegisState):

#     question = state["question"]

#     return {
#         "result": data_agent.total_revenue()
#     }


def knowledge_node(state: AegisState):

    result = knowledge_agent.answer_question(
        state["question"]
    )

    return {
        "result": result
    }


def route_after_classification(state: AegisState):

    return state["route"]


graph_builder = StateGraph(AegisState)

graph_builder.add_node(
    "classifier",
    classify_node
)

graph_builder.add_node(
    "data",
    data_node
)

graph_builder.add_node(
    "knowledge",
    knowledge_node
)

graph_builder.add_edge(
    START,
    "classifier"
)

graph_builder.add_conditional_edges(
    "classifier",
    route_after_classification,
    {
        "data": "data",
        "knowledge": "knowledge"
    }
)

graph_builder.add_edge(
    "data",
    END
)

graph_builder.add_edge(
    "knowledge",
    END
)

aegis_graph = graph_builder.compile()


# from langgraph.graph import StateGraph, START, END

# from app.orchestrator.state import AegisState


# def classify_node(state: AegisState):

#     question = state["question"].lower()

#     if any(
#         word in question
#         for word in [
#             "refund",
#             "policy",
#             "shipping",
#             "support"
#         ]
#     ):
#         route = "knowledge"

#     else:
#         route = "data"

#     return {
#         "route": route
#     }


# def data_node(state: AegisState):

#     return {
#         "result": "Data Agent will handle this request."
#     }


# def knowledge_node(state: AegisState):

#     return {
#         "result": "Knowledge Agent will handle this request."
#     }


# def route_after_classification(state: AegisState):

#     return state["route"]


# graph_builder = StateGraph(AegisState)

# graph_builder.add_node(
#     "classifier",
#     classify_node
# )

# graph_builder.add_node(
#     "data",
#     data_node
# )

# graph_builder.add_node(
#     "knowledge",
#     knowledge_node
# )

# graph_builder.add_edge(
#     START,
#     "classifier"
# )

# graph_builder.add_conditional_edges(
#     "classifier",
#     route_after_classification,
#     {
#         "data": "data",
#         "knowledge": "knowledge"
#     }
# )

# graph_builder.add_edge(
#     "data",
#     END
# )

# graph_builder.add_edge(
#     "knowledge",
#     END
# )

# aegis_graph = graph_builder.compile()