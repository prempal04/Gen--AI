import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() 
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY was not loaded from .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

@observe()
def get_weather(city: str):
    # TODO!: Do an actual API Call
    print("🔨 Tool Called: get_weather", city)
    
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"

@observe()
def add(x, y):
    print("🔨 Tool Called: add", x, y)
    return x + y


system_prompt = """
You are an helpful AI assitant who is specialized in resolving user query
You work on start, plan, action, observe mode. 
For the given user query and available tools, plan the step by step execution, based on the planning, select the relevent tool from teh available tool, and based on the tool selection you perform an action to call the tool.
Wait on the obesrvation and based on the observation from the tool call resolve the user query.

Rules:
1. Follow the strict JSON output as per output schema.
2. Always perform one step at a time and wait for next input.
3.  Carefully analyse the user query.


Output JSON Format: 
{{
    "step": "string", 
    "content": "string",
    "function": "The name of the function if the step is action",
    "input": "The input parameter for the function",
}}

Available tools:

example:

User query: what is the weather of new york city ?
Output: {{"step":"plan", "content": "the user is interested in weather data of new york city"}}
Output: {{"step":"plan", "content": "from the available tools i should call get_weather"}}
Output: {{"step":"action", "function": "get_weather", "input": "new york city"}}
Output: {{"step":"observe", "content": "12 degree celsius and cloudy"}}
Output: {{"step":"output", "content": "The weather of new york city is 12 degree celsius and cloudy "}}

"""

response = client.chat.completions.create(
    model="gemini-3.6-flash",
    response_format= {"type": "json_object"},
    messages=[
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": "what is the weather in chandigarh"},
        {"role": "assistant", "content": "continue to the next step"}
    ]
)


print(response.choices[0].message.content)