# server/app/ai/gemini_ai.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # This will load variables from the .env file

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from environment variables")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

def ask_gemini(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text
