# dto.py
from pydantic import BaseModel

class UploadUrlRequest(BaseModel):
    """
    Pydantic model for URL upload.

    This model is used to validate the URL provided by the user, which will be
    used to fetch content from the given URL, process it, and index it in Faiss.

    Attributes:
        url (str): The URL to fetch and index.
    """
    url: str
