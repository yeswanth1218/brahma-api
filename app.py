from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("GROQ_API_KEY")

# Initialize the client with the API key
client = Groq(api_key=api_key)

# FastAPI app instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Add a root route
@app.get("/")
async def read_root():
    return {"message": "Welcome to Connecting Dots R&D site. Begin your testing!"}

# Request model
class ChatRequest(BaseModel):
    content: str

@app.post("/generate-response")
async def generate_response(request: ChatRequest):
    try:
        # Generate completion
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": request.content,  # Dynamic content from request
                }
            ],
            temperature=0.6,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        # Collect response
        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
        
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app using the following command:
# uvicorn script_name:app --reload
