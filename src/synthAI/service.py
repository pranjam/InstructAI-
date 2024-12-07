from common.instructai import InstructAIQueryService
from fastapi import HTTPException
from synthAI.dto import MessageInput
from common.logger import logger

class InstructAIService:
    """
    Service class to interact with the InstructAIQueryService.
    Provides methods to query the InstructAI service for generating responses and maintaining session-based history.
    """

    def __init__(self):
        """
        Initializes the InstructAIService, which interacts with the InstructAIQueryService.
        It also initializes an in-memory database (`local_db`) to store session-based conversation history.

        Attributes:
            instructai_query_service (InstructAIQueryService): An instance of the InstructAIQueryService used for querying.
            local_db (dict): A dictionary storing session-based conversation history.
        """
        self.instructai_query_service = InstructAIQueryService()
        self.local_db = {}  # In-memory storage for session-based chat history

    def get_history_by_session_id(self, session_id):
        """
        Retrieves the conversation history for a given session ID.

        Args:
            session_id (str): The session identifier used to look up the conversation history.

        Returns:
            list: The list of conversation history for the specified session. If no history exists, returns an empty list.

        Raises:
            Exception: If an error occurs while retrieving the history.
        """
        try:
            if session_id in self.local_db:
                return self.local_db[session_id]
            else:
                return []
        except Exception as e:
            logger.error(f"Error retrieving history for session {session_id}: {e}")
            return []

    def update_history(self, session_id, chat_list):
        """
        Updates the conversation history for a given session ID.

        Args:
            session_id (str): The session identifier used to update the conversation history.
            chat_list (list): A list of chat messages (user's and AI's responses) to be added to the history.

        Raises:
            Exception: If an error occurs while updating the history.
        """
        try:
            if session_id in self.local_db:
                self.local_db[session_id].extend(chat_list)
            else:
                self.local_db[session_id] = chat_list
        except Exception as e:
            logger.error(f"Error updating history for session {session_id}: {e}")

    def get_modified_query(self, msg_input: MessageInput):
        """
        Modifies the user's query based on the conversation history for the given session ID.

        Args:
            msg_input (MessageInput): The input message containing the query and session ID.

        Returns:
            str: The modified query if the conversation history is long enough to provide context; otherwise, returns the original query.

        Raises:
            Exception: If an error occurs while modifying the query.
        """
        try:
            history = self.get_history_by_session_id(msg_input.session_id)
            if len(history) >= 2:
                modified_query = self.instructai_query_service.get_modified_userquery(msg_input.query, history)
                return modified_query
            return msg_input.query
        except Exception as e:
            logger.error(f"Error modifying query for session {msg_input.session_id}: {e}")
            return msg_input.query

    def generate_related_queries(self, query, answer):
        """
        Generates related queries based on the original query and the AI-generated answer.

        Args:
            query (str): The original user's query.
            answer (str): The AI-generated answer to the query.

        Returns:
            list: A list of related queries generated based on the original query and the answer.

        Raises:
            Exception: If an error occurs while generating related queries.
        """
        try:
            queries_text = self.instructai_query_service.get_related_queries(query, answer)
            queries_list = queries_text.split('||')
            return queries_list
        except Exception as e:
            logger.error(f"Error generating related queries for '{query}' and answer '{answer}': {e}")
            return []

    def get_answer_from_query(self, msg_input: MessageInput):
        """
        Queries the InstructAIQueryService with the given query and returns the generated answer along with related queries.

        Args:
            msg_input (MessageInput): The input message containing the query and session ID.

        Returns:
            dict: A dictionary containing the AI-generated answer and a list of related queries.

        Raises:
            HTTPException: If an error occurs during query processing or if an error occurs while interacting with the InstructAI service.
        """
        try:
            _modified_query = self.get_modified_query(msg_input)
            # Call the InstructAI service to get the answer for the query
            answer = self.instructai_query_service.query(_modified_query)
            related_queries = []
            if answer:
                related_queries = self.generate_related_queries(_modified_query, answer["answer"])

            # Update the conversation history
            _chat_list = [{"User": _modified_query}, {"AI": answer["answer"]}]
            self.update_history(msg_input.session_id, _chat_list)

            # Add related queries to the answer
            answer["rel_queries"] = related_queries
            return answer
        except Exception as e:
            logger.error(f"Error querying InstructAI for session {msg_input.session_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error querying InstructAI: {str(e)}")
