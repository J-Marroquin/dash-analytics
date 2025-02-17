import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class Logger:
    """
    A custom logger class that manages logging to both console and rotating log files.

    Attributes:
    -----------
        log_dir (str): Directory where log files will be stored. Defaults to 'logs'.
    """
    def __init__(self, log_dir='logs'):
        """
        Initializes the Logger class and sets up logging configuration.

        Args:
        -----
            log_dir (str): The directory where log files will be stored. Defaults to 'logs'.
        """
        self.log_dir = log_dir
        self.setup_logging()

    def setup_logging(self):
        """
        Sets up the logging configuration with a timed rotating file handler and console logging.

        - Creates the log directory if it doesn't exist.
        - Configures the log file to rotate at midnight and keep backups for 7 days.
        """
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        log_filename = os.path.join(self.log_dir, 'log_' + self.get_current_date() + '.txt')

        
        log_handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=7, encoding= 'utf-8-sig')
        log_handler.suffix = "%Y-%m-%d.txt"  
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,  
            format=log_format,
            handlers=[
                log_handler,  
                logging.StreamHandler()  
            ]
        )

    def get_current_date(self):
        """
        Retrieves the current date in the format 'YYYY-MM-DD'.

        Returns:
        --------
            str: The current date as a string.
        """
        return datetime.now().strftime("%Y-%m-%d")

    def log_info(self, message):
        """
        Logs an informational message.

        Args:
        -----
            message (str): The message to log.
        """
        logging.info(message)

    def log_warning(self, message):
        """
        Logs a warning message.

        Args:
        -----
            message (str): The message to log.
        """
        logging.warning(message)

    def log_error(self, message):
        """
        Logs an error message.

        Args:
        -----
            message (str): The message to log.
        """
        logging.error(message)

    def log_exception(self, exception):
        """
        Logs an exception with traceback information.

        Args:
        -----
            exception (Exception): The exception object to log.
        """
        logging.error("Excepción ocurrida", exc_info=exception)


# Uso de la clase Logger
if __name__ == "__main__":
    logger = Logger()

    # Registra algunos mensajes de ejemplo
    logger.log_info("Este es un mensaje de información.")
    logger.log_warning("Este es un mensaje de advertencia.")
    logger.log_error("Este es un mensaje de error.")
