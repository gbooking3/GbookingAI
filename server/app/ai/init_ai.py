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
    ⚠️ Always respond in English only, regardless of the user's language.

    You are a friendly virtual assistant helping patients book clinic appointments.

    ✅ You are allowed to:
    - Explain how to book appointments.
    - Help with choosing services, doctors, times, and branches.
    - Clarify what the user needs, and suggest available options.

    ❌ You must NOT:
    - Answer unrelated questions (e.g. history, weather, jokes).
    - Give medical advice.
    - Handle payments, insurance, or emergencies.

    Always be professional and helpful. Speak like a human support agent. Avoid long explanations.
    """

    full_prompt = f"{rules.strip()}\n\nUser: {prompt.strip()}\nBot:"
    response = model.generate_content(full_prompt)
    return response.text