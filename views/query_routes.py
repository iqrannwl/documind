from fastapi import APIRouter
from controllers import query_controller
from models.query import QueryRequest

router = APIRouter(tags=["Query"])

@router.post("/query")
async def query(payload: QueryRequest):
    return await query_controller.query_documents(payload)

@router.post("/query/stream")
async def query_stream(payload: QueryRequest):
    return await query_controller.query_stream(payload)
