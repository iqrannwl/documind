from fastapi import APIRouter, UploadFile, File
from typing import List
from controllers import document_controller
from models.document import DocumentCreate

router = APIRouter(tags=["Documents"])

@router.post("/documents")
async def add_documents(payload: DocumentCreate):
    return await document_controller.create_documents(payload)

@router.post("/documents/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    return await document_controller.upload_documents(files)

@router.get("/documents")
def list_docs():
    return document_controller.list_documents()

@router.delete("/documents/{doc_id}")
def delete_doc(doc_id: str):
    return document_controller.delete_document(doc_id)
