from pathlib import Path
from langchain_core.documents import Document


def load_schema_docs():
    docs=[]
    schema_path = Path(r"C:\Users\Administrator\Desktop\sql-ai-agent\rag\schema_docs")
    print(schema_path)
    for file in schema_path.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            docs.append(
                Document(
                    page_content=f.read(),
                    metadata={"table": file.stem}
                )
            )

    print(f"Loaded {len(docs)} schema documents.")
    print(docs[0].metadata.get("table"))
    return docs
    
