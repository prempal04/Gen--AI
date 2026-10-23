import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model='gemini-3.5-flash', contents='Why is the sky blue?'
)
print(response.text) 