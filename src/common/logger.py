import logging
import os


class Logger:
    """
    Logger class to handle logging configurations and create a logger instance.
    
    Attributes:
        logger (logging.Logger): Configured logger instance with file and console handlers.
    """

    def __init__(self):
        """
        Initializes a logging configuration and logger instance.

        This constructor sets up a logger with:
        - A file handler to write logs to a specified log file (defaults to 'default_logfile.log').
        - A console handler to print logs to the console.
        - Both handlers use the INFO log level.
        """
        try:
            # Get log file path from environment variable
            log_file_path = os.getenv('LOG_FILE_PATH', 'default_logfile.log')  # Default to 'default_logfile.log' if not set

            # Creating a logger instance
            self.logger = logging.getLogger(__name__)

            # Set the log level
            self.logger.setLevel(logging.INFO)

            # Create file handler to log messages to a file
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(logging.INFO)

            # Create console handler to print log messages to console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # Define log format for both handlers, including the calling file name
            formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

            # Set formatter for both handlers
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # Add handlers to the logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        
        except Exception as e:
            # Log error if logger setup fails
            logging.basicConfig(level=logging.ERROR)
            logging.error(f"Error initializing logger: {str(e)}")
            raise  # Re-raise the exception after logging it

    def get_logger(self):
        """
        Retrieves the configured logger instance.

        Returns:
            logging.Logger: Configured logger instance.
        """
        return self.logger


# Creating a singleton instance of Logger class
logger = Logger().get_logger()
