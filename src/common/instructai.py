from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from common.vector_db import FaissIndexer
from fastapi import HTTPException
from common.prompt import QueryPrompt  # Import the Enum for prompt template
from common.logger import logger
from pydantic import BaseModel


class InstructAIQueryService:
    """
    Service to handle querying and interacting with the InstructAI model using a vector database and GPT-4.

    Methods:
        query(query: str): Processes the user's query, retrieves relevant documents, and invokes GPT-4 to generate an answer.
        get_modified_userquery(query: str, history: str): Reformats the user's query based on chat history and invokes GPT-4 for a modified response.
        get_related_queries(query: str, answer: str): Generates a set of related queries based on the user's question and answer.
    """

    def __init__(self):
        """
        Initializes the InstructAIQueryService with a FAISS indexer and a GPT-4 model for question answering.
        """
        # Load the FAISS indexer instance to interact with the vector database
        self.vector_db = FaissIndexer()

        # Initialize the GPT model for question answering
        self.llm = ChatOpenAI(model="gpt-4o")


    def query(self, query: str):
        """
        Processes the user's query by retrieving relevant documents from the vector database
        and using GPT-4 to generate an answer.

        Args:
            query (str): The query/question provided by the user.

        Returns:
            dict: A dictionary containing the generated answer and the source documents used.

        Raises:
            HTTPException: If an error occurs while processing the query.
        """
        try:
            print(query)
            # Use the retriever to get relevant documents
            retrieved_docs = self.vector_db.as_retriever().get_relevant_documents(query)
            formatted_prompt = QueryPrompt.QUERY_PROMPT.value.format(question=query, context=retrieved_docs)
            _src_docs = []
            for i, doc in enumerate(retrieved_docs, start=1):
                _src_docs.append(doc.metadata.get("source"))

            # Execute the query through the RetrievalQA chain
            response = self.llm.invoke(formatted_prompt)
            print(response)

            return {
                "answer": response.content,
                "source_documents": _src_docs
            }

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

    def get_modified_userquery(self, query, history):
        """
        Reformats the user's query based on chat history and generates a modified response using GPT-4.

        Args:
            query (str): The query/question to be modified.
            history (str): The chat history to provide context for the modification.

        Returns:
            str: The modified query after processing.
        """
        try:
            formatted_prompt = QueryPrompt.REFORMATTING_QUERY.value.format(question=query, chat_history=history)
            response = self.llm.invoke(formatted_prompt)
            return response.content
        except Exception as e:
            logger.error(f"Error processing modify query: {str(e)}")
            return query

    def get_related_queries(self, query, answer):
        """
        Generates a set of related queries based on the user's question and the answer provided.

        Args:
            query (str): The original query/question asked by the user.
            answer (str): The answer generated for the original query.

        Returns:
            str: A string containing related queries based on the provided question and answer.
        """
        try:
            formatted_prompt = QueryPrompt.RELATED_QUERIES.value.format(question=query, answer=answer)
            response = self.llm.invoke(formatted_prompt)
            return response.content
        except Exception as e:
            logger.error(f"Error processing related queries: {str(e)}")
            return query
