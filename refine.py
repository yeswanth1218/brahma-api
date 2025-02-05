from groq import Groq
import os
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
refine_client = Groq(api_key=API_KEY)

async def refine_input(user_input: str) -> str:
    try:
        response = refine_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": (
                    "Your ONLY task is to correct spelling and grammar errors in the given input. "
                    "Do NOT change the meaning, do NOT rephrase, and do NOT answer any questions. "
                    "Simply return the corrected version of the input exactly as it was given, except for grammatical fixes."
                )},
                {"role": "user", "content": user_input}
            ],
            temperature=0,  # Ensures deterministic output
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        # Extract corrected text
        refined_text = response.choices[0].message.content.strip()

        return refined_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Input refinement failed: {str(e)}")
