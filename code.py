from fastapi import FastAPI
from pydantic import BaseModel
import openai
import json

app = FastAPI()

# 🔐 Replace this with your actual API key
openai.api_key = "your_openai_api_key"

# --------------------
# Function Implementations (Dummy data for now)
# --------------------

def find_tiffin_services(location: str):
    return f"Tiffin services in {location}: 'Maa Tiffin', 'Healthy Meals', 'QuickLunch'."

def find_room_near_office(location: str):
    return f"Rental rooms near {location}: 'PG Nest', 'CoLive Comfort', 'BudgetStay'."

def find_colleagues_nearby(company_name: str):
    return f"Colleagues from {company_name} nearby: 'Anil Kumar', 'Sara Ahmed', 'John Doe'."

def estimate_local_costs(city: str):
    return f"Estimated costs in {city}: Auto: ₹100/day, Food: ₹250/day, Stay: ₹700/night."

def assess_safety(city: str):
    return f"{city} has a safety rating of 3.8/5. Safe during day, moderate caution at night."

def trip_planner(destination: str):
    return f"Trip plan for {destination}: Day 1 - Explore city, Day 2 - Visit landmarks, Est. cost ₹6000."

def compare_cities(city1: str, city2: str):
    return f"{city1} vs {city2}: {city1} is cheaper, but {city2} has better infrastructure and safety."

# --------------------
# Request Body Schema
# --------------------

class UserRequest(BaseModel):
    user_query: str

# --------------------
# FastAPI Route
# --------------------

@app.post("/chat")
async def chat_with_llm(user_req: UserRequest):
    # Define all LLM-callable functions
    functions = [
        {
            "name": "find_tiffin_services",
            "description": "Finds tiffin providers in a specific location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                },
                "required": ["location"],
            },
        },
        {
            "name": "find_room_near_office",
            "description": "Finds rental rooms or PGs near a workplace",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                },
                "required": ["location"],
            },
        },
        {
            "name": "find_colleagues_nearby",
            "description": "Finds colleagues working in the same company nearby",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {"type": "string"},
                },
                "required": ["company_name"],
            },
        },
        {
            "name": "estimate_local_costs",
            "description": "Estimates local transport, food, and living costs",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                },
                "required": ["city"],
            },
        },
        {
            "name": "assess_safety",
            "description": "Provides a safety rating for a city or area",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                },
                "required": ["city"],
            },
        },
        {
            "name": "trip_planner",
            "description": "Creates a travel plan and cost estimate",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {"type": "string"},
                },
                "required": ["destination"],
            },
        },
        {
            "name": "compare_cities",
            "description": "Compares two cities for living, job, or travel",
            "parameters": {
                "type": "object",
                "properties": {
                    "city1": {"type": "string"},
                    "city2": {"type": "string"},
                },
                "required": ["city1", "city2"],
            },
        },
    ]

    messages = [{"role": "user", "content": user_req.user_query}]

    # Call GPT with function definitions
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        functions=functions,
        function_call="auto"
    )

    message = response["choices"][0]["message"]

    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        arguments = json.loads(message["function_call"]["arguments"])

        # Map of function names to actual functions
        function_map = {
            "find_tiffin_services": find_tiffin_services,
            "find_room_near_office": find_room_near_office,
            "find_colleagues_nearby": find_colleagues_nearby,
            "estimate_local_costs": estimate_local_costs,
            "assess_safety": assess_safety,
            "trip_planner": trip_planner,
            "compare_cities": compare_cities,
        }

        func = function_map.get(function_name)

        if func:
            result = func(**arguments)
        else:
            result = "Function not implemented."

        return {"response": result}

    else:
        return {"response": message["content"]}
