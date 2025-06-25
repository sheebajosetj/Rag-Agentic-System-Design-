from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Document(BaseModel):
    title: str
    publication_date: datetime
    executive_order_number: Optional[str] = None
    
    summary: Optional[str] = None



def process_documents(raw_docs: List[dict]) -> List[Document]:
    processed = []
    for doc in raw_docs:
        try:
            processed.append(Document(
                title=doc.get("title"),
                publication_date=datetime.strptime(doc.get("publication_date"), "%Y-%m-%d"),
                executive_order_number=doc.get("document_number"),  # fallback
                
                summary=doc.get("abstract") or "No summary available"
            ))
        except Exception as e:
            print(f"Skipping doc due to error: {e}")
            continue
    return processed




