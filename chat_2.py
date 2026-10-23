import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and then resolve the user query 

For the given user input, analyse the input and breakdown the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyse, you think, you again think for several times and return an output with expalantion 

Follow the steps in sequence this is "analyse", "think", "output", "validate" and finally "result" 

Rules:
1. Follow the strict JSON output as per output schema.
2. Always perform one step at a time and wait for next input.
3.  Carefully analyse the user query.

Output Format: {{step: "string", content: "string" }}

Example:
Input: What is 2+2 ?
Output: {{step: "analyze", content: "Alright, The user is interested in maths query and he is asking a basic arithmetic operation"}}
Output: {{step: "think", contnet: "To perform the addition i must go from left to right and add all the operands and then finally you validate the output as well before giving final result "}}
Output: {{step: "output", content: "The final output is 4"}}
Output: {{step: "validate", content: "seems like 4 is correct answer for 2+2"}}
Output:{{step:"result", contnet: "2+2=4 and that is calculated by adding all the numbers"}} }}
"""

response_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "step": {
                "type": "string",
                "enum": [
                    "analyze",
                    "think",
                    "output",
                    "validate",
                    "result"
                ]
            },
            "content": {
                "type": "string"
            }
        },
        "required": ["step", "content"],
        "additionalProperties": False
    }
}

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="What is 3 + 4 * 5?",
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="application/json",
        response_schema=response_schema
    )
)

# Gemini returns JSON as text
result = json.loads(response.text)

# Python object
print(result)

# Proper formatted JSON
print(json.dumps(result, indent=2))