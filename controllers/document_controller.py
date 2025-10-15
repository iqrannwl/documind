import os
from typing import List

from fastapi import UploadFile, HTTPException
from models.document import DocumentCreate, DocumentResponse, DocumentListResponse
from services.vector_store_service import VectorStoreService
from utils.file_loader import load_pdf, load_text

vector_store = VectorStoreService()

async def create_documents(documents: DocumentCreate):
    try:
        result = await vector_store.index_documents(documents.documents)
        return DocumentResponse(
            success=True,
            message=f"Indexed {len(documents.documents)} documents.",
            document_ids=result["document_ids"],
            chunks_created=result["chunks_created"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def upload_documents(files: List[UploadFile]):
    try:
        all_docs = []
        for file in files:
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in [".pdf", ".txt", ".md"]:
                raise HTTPException(status_code=400, detail=f"Unsupported file: {ext}")
            content = await file.read()
            text = load_pdf(content) if ext == ".pdf" else load_text(content)
            all_docs.append({"title": file.filename, "content": text})

        result = await vector_store.index_documents(all_docs)
        return DocumentResponse(
            success=True,
            message=f"Uploaded & indexed {len(files)} files.",
            document_ids=result["document_ids"],
            chunks_created=result["chunks_created"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def list_documents():
    docs = vector_store.list_documents()
    return DocumentListResponse(success=True, count=len(docs), documents=docs)

def delete_document(doc_id: str):
    success = vector_store.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"success": True, "message": f"Deleted document {doc_id}"}
