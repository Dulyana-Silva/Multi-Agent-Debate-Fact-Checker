
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Loading API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

#Creating a Gemini client 
# client --> It's like a connection interface to the Gemini service. It handles the API requests and responses.
client = genai.Client(api_key=api_key)

#Define the role of the assistant
system_instruction = """You are a careful fact-checking assistant.

Your responsibilities:
1. Analyze the user's claim.
2. Identify potentially misleading information.
3. Explain your reasoning clearly.
4. State when you are uncertain.
5. Never invent sources or citations.
"""

#Claim to anaylze
claim= "Humans use only 10 percent of their brains."


#Ask Gemini to anayze the claim
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents= claim,
    config= types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.2,
    )
)

#Printing the response
print("\nClaim:",claim)
print("\nAnalysis:",response.text)