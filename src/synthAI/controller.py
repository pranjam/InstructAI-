from fastapi import APIRouter, HTTPException
from synthAI.service import InstructAIService
from synthAI.dto import MessageInput
router = APIRouter()

# Create an instance of the InstructAIService
instructai_service = InstructAIService()

@router.post("/query")
async def query_instructai(msg_input:MessageInput):
    """
    Endpoint for querying the InstructAI service with a user query.

    Args:
        query (str): The query string provided by the user.

    Returns:
        str: The response from the InstructAI query service.
    """
    try:
        # Call the service to get the answer for the query
        result = instructai_service.get_answer_from_query(msg_input)
        return {"answer": result}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
