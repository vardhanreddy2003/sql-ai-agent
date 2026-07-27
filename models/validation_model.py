from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from .Evaluation import evaluation

def validation_model_creation():
    llm = HuggingFaceEndpoint(
        repo_id="deepseek-ai/DeepSeek-V4-Flash",
        task = "text-generation"
    )

    model = ChatHuggingFace(
        llm=llm

    )
    
    return model