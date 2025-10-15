from fastapi import APIRouter
from controllers.health_controller import HealthController

router = APIRouter()

@router.get("/", summary="Health check endpoint")
def health_check():
    """
    Returns API and dependency health status.
    """
    return HealthController.get_health_status()
