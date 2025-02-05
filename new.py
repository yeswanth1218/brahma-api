# # refine.py
# from typing import Any
# import os
# from dotenv import load_dotenv
# from groq import Groq  # Assuming Groq can be used for refinement as well
# from fastapi import HTTPException

# load_dotenv()

# API_KEY = os.getenv("GROQ_API_KEY")
# refine_client = Groq(api_key=API_KEY)

# async def refine_input(user_input: str) -> str:
#     try:
#         # Call Groq API to refine input
#         response = refine_client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {"role": "system", "content": "You are an assistant that corrects only spelling and grammar."},
#                 {"role": "user", "content": user_input}
#             ],
#             temperature=0.2,
#             max_tokens=1024,
#             top_p=1,
#             stream=False,
#             stop=None,
#         )

#         # Correct way to access response content
#         refined_text = response.choices[0].message.content.strip()

#         return refined_text
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Input refinement failed: {str(e)}")
