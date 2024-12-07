from pydantic import BaseModel

class MessageInput(BaseModel):
    """The input for message"""
    query: str
    session_id : str