from fastapi import FastAPI
from views import health_routes
from config import Config


app = FastAPI(title=Config.APP_NAME, version=Config.VERSION)

# Health check
app.include_router(health_routes.router, prefix="/health", tags=["Health"])
