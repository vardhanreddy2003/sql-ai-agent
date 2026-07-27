from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint

def query_generator():
    llm=HuggingFaceEndpoint(
        model="deepseek-ai/DeepSeek-V4-Flash",
        task="task-generation"
    )
    model = ChatHuggingFace(
        llm=llm

    )
    return model