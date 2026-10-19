
# First LLM API calling using python

import os
from dotenv import load_dotenv
from google import genai

# Loading API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

#Creating a Gemini client 
# client --> It's like a connection interface to the Gemini service. It handles the API requests and responses.
client = genai.Client(api_key=api_key)

#Calling the LLM model to generate content based on the provided prompt
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Explain what an AI agent is in 3 simple sentences."
)

#Printing the response
print(response.text)