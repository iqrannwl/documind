import json
from fastapi.responses import StreamingResponse

from models.query import QueryRequest, QueryResponse
from services.vector_store_service import VectorStoreService
from services.llm_service import LLMService

vector_store = VectorStoreService()
llm_service = LLMService()

async def query_documents(query: QueryRequest):
    chunks = await vector_store.search(query.question, query.top_k)
    if not chunks:
        return QueryResponse(success=True, answer="No relevant info found.", sources=[], question=query.question)
    answer = await llm_service.generate_answer(query.question, chunks, query.temperature)
    return QueryResponse(success=True, answer=answer, sources=chunks, question=query.question)

async def query_stream(query: QueryRequest):
    chunks = await vector_store.search(query.question, query.top_k)
    if not chunks:
        async def empty():
            yield json.dumps({"type": "answer", "content": "No relevant info found"}) + "\n"
        return StreamingResponse(empty(), media_type="application/x-ndjson")

    async def stream():
        yield json.dumps({"type": "sources", "content": chunks}) + "\n"
        async for chunk in llm_service.generate_answer_stream(query.question, chunks, query.temperature):
            yield json.dumps({"type": "answer", "content": chunk}) + "\n"

    return StreamingResponse(stream(), media_type="application/x-ndjson")
