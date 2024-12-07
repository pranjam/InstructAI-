import faiss
import numpy as np
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from fastapi import HTTPException
from common.logger import logger
import uuid

class Singleton:
    """
    A base class that implements the Singleton design pattern.
    Ensures that only one instance of any class that inherits from it exists.
    """
    _instances = {}

    def __new__(cls, *args, **kwargs):
        """
        Ensures that only one instance of the class exists.
        If an instance already exists, it will return that instance.
        Otherwise, it will create a new one.

        Args:
            *args: Positional arguments for the instance initialization.
            **kwargs: Keyword arguments for the instance initialization.
        
        Returns:
            object: The single instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls)
        return cls._instances[cls]

class FaissIndexer(Singleton):
    """
    A class that handles the indexing and querying of documents in a Faiss index.
    The documents are embedded using OpenAI embeddings before being indexed in Faiss.
    This class also provides methods to fetch content from URLs, index it, and query the index for relevant results.
    """
    def __init__(self, faiss_index_file_path: str = "faiss_index_file.index"):
        """
        Initializes the FaissIndexer class.

        Args:
            faiss_index_file_path (str): Path where the Faiss index will be stored or loaded from.
        """
        self.embeddings = OpenAIEmbeddings()
        self.faiss_index = None
        self.faiss_index_file_path = faiss_index_file_path
        self.documents = []  # To store the original documents
        self.vector_store = None
        self.load_faiss_index()

    def load_faiss_index(self):
        """
        Loads the Faiss index from disk if it exists, otherwise initializes the index as None.
        This method is called during initialization to ensure the index is available.

        If the Faiss index is not found at the specified path, it will initialize an empty Faiss index.
        """
        try:
            if os.path.exists(self.faiss_index_file_path):
                # Load the vector store
                self.vector_store = FAISS.load_local(self.faiss_index_file_path, self.embeddings, allow_dangerous_deserialization=True)
                logger.info(f"Faiss index loaded from {self.faiss_index_file_path}")
            else:
                # Create a new index and vector store
                index = faiss.IndexFlatL2(len(self.embeddings.embed_query("hello world")))  # Use the embedding dimension
                docstore = InMemoryDocstore()
                self.vector_store = FAISS(embedding_function=self.embeddings, index=index, docstore=docstore, index_to_docstore_id={})
                logger.info("Faiss index not found, initialized a new vector store.")
        except Exception as e:
            logger.error(f"Error loading Faiss index: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error loading Faiss index: {str(e)}")

    def save_faiss_index(self):
        """
        Saves the Faiss index to disk after modification.
        """
        try:
            if self.vector_store:
                self.vector_store.save_local(self.faiss_index_file_path)
                logger.info(f"Faiss index saved to {self.faiss_index_file_path}")
            else:
                raise HTTPException(status_code=500, detail="Faiss index is None, cannot save.")
        except Exception as e:
            logger.error(f"Error saving Faiss index: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error saving Faiss index: {str(e)}")

    def fetch_url_content(self, url: str):
        """
        Fetches the content of a webpage from the given URL.
        
        Args:
            url (str): The URL of the webpage to fetch content from.

        Returns:
            list: List of documents containing the fetched content.

        Raises:
            HTTPException: If there is an error fetching the content from the URL.
        """
        try:
            loader = UnstructuredURLLoader([url])
            documents = loader.load()  # Load documents from the URL
            logger.info(f"Document loaded successfully!: {documents}")
            return documents
        except Exception as e:
            logger.error(f"Error fetching content from URL: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching content from URL: {str(e)}")

    def index_documents(self, documents):
        """
        Indexes the provided documents into the Faiss index after embedding them using OpenAI embeddings.

        Args:
            documents (list): List of documents to index.
        
        Raises:
            HTTPException: If there is an error during indexing.
        """
        try:
            # Extract text content from the documents
            texts = [doc.page_content for doc in documents]

            # Add documents to the vector store, along with the metadata
            ids = [str(uuid.uuid4()) for _ in range(len(documents))]
            self.vector_store.add_texts(texts, metadatas=[doc.metadata for doc in documents], ids=ids)

            # Store documents for later retrieval
            self.documents.extend(documents)

            # Save the Faiss index after adding the documents
            self.save_faiss_index()

        except Exception as e:
            logger.error(f"Error indexing documents in Faiss: {str(e)}")

    def query_faiss(self, query: str):
        """
        Queries the Faiss index with a given query string.

        Args:
            query (str): The query string to search for.

        Returns:
            list: List of results containing the closest matching documents.

        Raises:
            HTTPException: If the Faiss index is empty or there is an error during the query.
        """
        try:
            if not self.vector_store:
                raise HTTPException(status_code=400, detail="Faiss index is empty. Please index documents first.")

            results = self.vector_store.similarity_search(query, k=5)

            # Return the closest matching documents along with their metadata
            return [{"document": doc, "distance": dist, "metadata": doc.metadata} for doc, dist in results]

        except Exception as e:
            logger.error(f"Error querying Faiss: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error querying Faiss: {str(e)}")

    def as_retriever(self):
        """
        Returns the Faiss index as a retriever for document retrieval.

        Returns:
            object: The Faiss retriever instance.
        """
        return self.vector_store.as_retriever()
