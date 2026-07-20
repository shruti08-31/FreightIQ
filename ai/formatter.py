import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"

def format_response(user_query, context):
    if not context:
        return "Information is not available in the current CDX database or the query parameters were incomplete."

    prompt = f"""User Question:
{user_query}

Database Results:
{json.dumps(context, indent=2)}

RULES
1. Answer ONLY the user's question.
2. Use ONLY the supplied database/service results.
3. Never recommend anything not returned by the services.
4. If the user asked only one thing, ignore the remaining data.
5. Do not invent information.
6. Never add report sections.
7. Never explain services that were not requested.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a precise AI logistics assistant. You format data strictly according to the provided rules."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "An error occurred while generating the logistics response."
