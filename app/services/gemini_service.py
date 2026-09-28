# from google import genai
# from dotenv import load_dotenv

# load_dotenv()

# client = genai.Client()


# def classify_question(question: str):

#     response = client.models.generate_content(
#         model="gemini-3.8-flash",
#         contents=question
#     )

#     return response.text

# the below code was facing high demand with gemini 3.6 and 3.8 flash models, the above code is for plain testing
import json

from google import genai
from dotenv import load_dotenv

from app.models.ai_models import AegisOperation
from app.data_agents.data_agent import DataAgent

from app.models.ai_models import (
    AegisOperation,
    AegisRoute
)

load_dotenv()

client = genai.Client()

data_agent = DataAgent()

def total_revenue_tool():
    return data_agent.total_revenue()


def monthly_revenue_tool():
    return data_agent.monthly_revenue()


def monthly_profit_tool():
    return data_agent.monthly_profit()

TOOLS = [
    total_revenue_tool,
    monthly_revenue_tool,
    monthly_profit_tool,
]

def ask_with_tools(question: str):

    tools = [
        {
            "type": "function",
            "name": "total_revenue_tool",
            "description": "Returns the total revenue from the business orders.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "type": "function",
            "name": "monthly_revenue_tool",
            "description": "Returns revenue grouped by month.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "type": "function",
            "name": "monthly_profit_tool",
            "description": "Returns profit grouped by month.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    ]

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=question,
        tools=tools,
    )

    function_call = next(
        step
        for step in interaction.steps
        if step.type == "function_call"
    )

    if function_call.name == "total_revenue_tool":
        result = total_revenue_tool()

    elif function_call.name == "monthly_revenue_tool":
        result = monthly_revenue_tool()

    elif function_call.name == "monthly_profit_tool":
        result = monthly_profit_tool()

    else:
        raise ValueError(
            f"Unknown function: {function_call.name}"
        )

    final_interaction = client.interactions.create(
        model="gemini-3.8-flash",
        previous_interaction_id=interaction.id,
        tools=tools,
        input=[
            {
                "type": "function_result",
                "name": function_call.name,
                "call_id": function_call.id,
                "result": [
                    {
                        "type": "text",
                        "text": json.dumps(result),
                    }
                ],
            }
        ],
    )

    return final_interaction.output_text

def classify_question(question: str) -> AegisOperation:

    prompt = f"""
You are the decision layer of Aegis.

Choose exactly one operation from these allowed operations:

- total_revenue
- monthly_revenue
- monthly_profit

User question:
{question}
"""

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": AegisOperation.model_json_schema(),
        },
    )

    return AegisOperation.model_validate_json(
        interaction.output_text
    )

def classify_route(question: str):

    prompt = f"""
Classify the user's request into exactly one route:

data
knowledge

Use "data" for questions requiring business data,
analytics, revenue, sales, orders, customers, or calculations.

Use "knowledge" for questions requiring company policies,
documentation, procedures, shipping, refunds, or support information.

Return only the structured route.

User question:
{question}
"""

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": AegisRoute.model_json_schema()
        }
    )

    return AegisRoute.model_validate_json(
        response.output_text
    )

# def classify_route(question: str):

#     prompt = f"""
# Classify the user's request into exactly one route:

# data
# knowledge

# Use "data" for questions requiring business data,
# analytics, revenue, sales, orders, customers, or calculations.

# Use "knowledge" for questions requiring company policies,
# documentation, procedures, shipping, refunds, or support information.

# Return only the structured route.

# User question:
# {question}
# """

#     response = client.interactions.create(
#         model="gemini-3.8-flash",
#         input=prompt,
#         response_format={
#             "type": "json_schema",
#             "json_schema": {
#                 "name": "AegisRoute",
#                 "schema": AegisRoute.model_json_schema()
#             }
#         }
#     )

#     return AegisRoute.model_validate_json(
#         response.output_text
#     )

def execute_operation(operation: AegisOperation):

    if operation.operation == "total_revenue":
        return data_agent.total_revenue()

    if operation.operation == "monthly_revenue":
        return data_agent.monthly_revenue()

    if operation.operation == "monthly_profit":
        return data_agent.monthly_profit()

    raise ValueError(
        f"Unsupported operation: {operation.operation}"
    )



# previous code below:
# from google import genai
# from dotenv import load_dotenv

# load_dotenv()

# client = genai.Client()


# def ask_gemini(question: str):

#     response = client.models.generate_content(
#         model="gemini-3.6-flash",
#         contents=question
#     )

#     return response.text