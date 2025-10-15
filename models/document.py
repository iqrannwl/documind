from pydantic import BaseModel
from typing import List, Optional

class Document(BaseModel):
    title: str
    content: str

class DocumentCreate(BaseModel):
    documents: List[Document]

class DocumentResponse(BaseModel):
    success: bool
    message: str
    document_ids: Optional[List[str]] = None
    chunks_created: Optional[int] = None

class DocumentListResponse(BaseModel):
    success: bool
    count: int
    documents: List[str]
