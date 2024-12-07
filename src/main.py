import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from dotenv import load_dotenv
# Load environment variables from a .env file
load_dotenv()

import uvicorn
from common.vector_db import FaissIndexer  # Import FaissIndexer class from vector_db.py
from ingestion.router import router as api_router
from synthAI.router import router as instructai_router



# Initialize FastAPI app
app = FastAPI()

# Include routers for different APIs
app.include_router(api_router)
app.include_router(instructai_router)

# Initialize the FaissIndexer instance with the specified file path for Faiss index
faiss_indexer = FaissIndexer(faiss_index_file_path="faiss_index_file")

if __name__ == "__main__":
    # Fetch the port from environment variables, default to 8000 if not set
    port = int(os.getenv("PORT", 8000))

    # Run the app with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
