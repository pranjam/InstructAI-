from fastapi import Depends, HTTPException, Header
import os

def api_key_dependency(x_api_key: str = Header(None)):
    """
    Dependency function to validate the API key from the request header.

    Args:
        x_api_key (str, optional): The API key provided in the request header. Defaults to None.

    Raises:
        HTTPException: If the provided API key does not match the one stored in the environment variables,
                        an HTTPException with a 401 status code is raised.

    Returns:
        None: This function does not return a value. It either raises an HTTPException or allows the request to proceed.
    """
    try:
        if x_api_key != os.environ["API_KEY"]:
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")
    except KeyError:
        # Handle the case where the environment variable is not set
        raise HTTPException(status_code=500, detail="Internal Server Error: API_KEY not configured in environment")
    except Exception as e:
        # Catch any other exceptions that might occur
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
