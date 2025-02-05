# app.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
from refine import refine_input
from database import AsyncSessionLocal, engine
from models import UserInput
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import pytz
import uuid
import asyncio

# Load environment variables from the .env file
load_dotenv()

# Get the API key and DATABASE_URL from the environment variables
api_key = os.getenv("GROQ_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize the client with the API key
client = Groq(api_key=api_key)

# FastAPI app instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your React app's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Add a root route
@app.get("/")
async def read_root():
    return {"message": "Welcome to Connecting Dots R&D site. Begin your testing!"}

# Request model
class ChatRequest(BaseModel):
    content: str

# Function to save user input to the database
async def save_user_input(refined_input: str):
    async with AsyncSessionLocal() as session:
        try:
            # Get current time in IST and remove timezone info
            ist = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(ist).replace(tzinfo=None)  # Convert to naive datetime

            user_input = UserInput(
                refined_user_input=refined_input,
                time_and_date=current_time,  # Now this is naive
                consider=True
            )
            session.add(user_input)
            await session.commit()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            await session.rollback()

# Function to refine input and save to DB
async def process_user_input(user_input: str):
    refined = await refine_input(user_input)
    await save_user_input(refined)

@app.post("/generate-response")
async def generate_response(request: ChatRequest, background_tasks: BackgroundTasks):
    try:
        # Refine the input once for both DB saving and LLM processing
        refined_user_input = await refine_input(request.content)

        # Schedule the background task to save the refined input in the DB
        background_tasks.add_task(save_user_input, refined_user_input)

        # Generate completion from LLM using the refined input
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": refined_user_input,
                }
            ],
            temperature=0.6,
            max_tokens=8192,
            top_p=1,
            stream=False,  # Ensure stream is False
            stop=None,
        )

        # Extract the response text correctly
        response_text = completion.choices[0].message.content.strip()

        return {"response": response_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

