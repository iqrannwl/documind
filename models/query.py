from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str
    top_k: int = 3
    temperature: float = 0.7

class QueryResponse(BaseModel):
    success: bool
    answer: str
    sources: Optional[List[str]] = None
    question: str
