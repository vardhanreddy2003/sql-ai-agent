from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()

def model_creation():
  model=ChatGoogleGenerativeAI(
          model="gemini-3.1-flash-lite",
          temperature=0,
          google_api_key=os.environ.get("google_api_key")
      )
  return model