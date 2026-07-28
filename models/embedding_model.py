
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

def embedding_model():
    return GoogleGenerativeAIEmbeddings(model="gemini-embedding-2", api_key=os.environ.get("google_api_key"))