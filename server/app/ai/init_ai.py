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
    rules = """
  
        You are a friendly virtual assistant, helping patients schedule appointments at a clinic.

        ✅ You are allowed to:
        - Explain how to schedule appointments.
        - When listing multiple items (such as departments, services, doctors, available dates, or available hours), **always** present them neatly (even when they contain one item):
            - Each item should be on a new line.
        - If change instructions ("change department", "change doctor", "change service", "change date", "change time") are included, show only the ones present.

        ❌ You are not allowed to:
        - Answer unrelated questions (e.g., history, weather, jokes).
        - Provide medical advice.
        - **change or modify backend message**
        - Handle payments, insurance, or urgent cases.

        ✅ Style Rules:
            - Always be professional and helpful.
            - Speak like a human service representative.
            - Avoid long explanations or unnecessary text.
        """


    full_prompt = f"{rules.strip()}\n\nUser: {prompt.strip()}\nBot:"
    response = model.generate_content(full_prompt)
    return response.text