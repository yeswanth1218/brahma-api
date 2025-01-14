from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("GROQ_API_KEY")

# Initialize the client with the API key
client = Groq(api_key=api_key)

completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": "I want to build an application which manages context (context management system) on top of an opemsource LLM. This is to tackle the limitation of LLM's token issues and lack of memory issue"
        }
    ],
    temperature=0.6,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
