from langchain_google_genai import ChatGoogleGenerativeAI
def model_creation():
  model=ChatGoogleGenerativeAI(
          model="gemini-3.1-flash-lite",
          temperature=0
      )
  return model