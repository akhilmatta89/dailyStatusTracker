# Configure the logging_lib
import logging

class Logger:

    def get_logger(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        return logging