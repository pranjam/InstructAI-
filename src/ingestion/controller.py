from fastapi import APIRouter, HTTPException, Depends
from ingestion.service import FaissIndexerService
from ingestion.dto import UploadUrlRequest
from common.logger import logger
router = APIRouter()

# Instantiate FaissIndexerService
faiss_service = FaissIndexerService()

@router.post("/url")
async def upload_url(request: UploadUrlRequest):
    """
    Endpoint to fetch content from a URL and index the documents in Faiss.

    Args:
        request (UploadUrlRequest): The URL to fetch and index.

    Returns:
        dict: A success message indicating the URL has been indexed.

    Raises:
        HTTPException: If there is an error during the URL upload and indexing process.
    """
    try:
        result = faiss_service.upload_url_and_index(request.url)
        logger.info(f"{request.url} uploaded successfully!")
        return result
    except HTTPException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Failed to upload and index the URL: {str(e)}")
