from fastapi import APIRouter, Depends
from ingestion.controller import router as controller_router
from common.auth import api_key_dependency  # Assuming api_key_dependency is in a separate file

router = APIRouter()

# Apply the API key check globally to all routes in this router
router.include_router(controller_router, prefix="/ingestion", tags=["ingestion Operations"], dependencies=[Depends(api_key_dependency)])

