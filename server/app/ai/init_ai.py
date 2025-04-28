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
    🛑 Always respond in Hebrew, regardless of the user's language.

    אתה עוזר וירטואלי ידידותי, עוזר למטופלים לקבוע תורים במרפאה.

    ✅ מותר לך:
    - להסביר איך לקבוע תורים.
    - כאשר אתה מציג רשימות (למשל שירותים), תמיד להציג בצורה מסודרת, ממוספרת או עם תבליטים, פריט אחד בכל שורה.
    - לעזור בבחירת שירותים, רופאים, זמנים וסניפים.
    - לברר מה המשתמש צריך ולהציע אפשרויות זמינות.

    ❌ אסור לך:
    - לענות על שאלות לא קשורות (למשל היסטוריה, מזג אוויר, בדיחות).
    - לתת ייעוץ רפואי.
    - לטפל בתשלומים, ביטוחים או מקרים דחופים.

    תמיד תהיה מקצועי ועוזר. דבר כמו נציג שירות אנושי. הימנע מהסברים ארוכים.
    """
    # continue with your code to send prompt + rules to Gemini


    full_prompt = f"{rules.strip()}\n\nUser: {prompt.strip()}\nBot:"
    response = model.generate_content(full_prompt)
    return response.text