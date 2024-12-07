from fastapi import APIRouter, Depends
from synthAI.controller import router as instructai_controller
from common.auth import api_key_dependency 

router = APIRouter()

# Include the controller with routes
router.include_router(instructai_controller, prefix="/instructai", tags=["InstructAI"],dependencies=[Depends(api_key_dependency)])
