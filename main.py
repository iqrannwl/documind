from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings
from views import document_routes, query_routes, health_routes

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered document question answering using vector search and LLMs"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers (Views)
app.include_router(health_routes.router, prefix="/api/v1")
app.include_router(document_routes.router, prefix="/api/v1")
app.include_router(query_routes.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": f"{settings.PROJECT_NAME} running!", "version": settings.VERSION}
