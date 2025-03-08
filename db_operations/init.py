import os.path
import sqlite3

import db_operations.constants
from logging_lib.logging_lib import Logger

Logger = Logger().get_logger()

class Init:

    def intialize_db(self):
        try:
            conn = sqlite3.connect(db_operations.constants.DB_PATH)

            cursor = conn.cursor()
            cursor.execute(db_operations.constants.CREATE_TABLE)
            Logger.info("Initialized successfully")
            conn.commit()
            conn.close()
        except Exception as ex:
            Logger.error("Some error occurred while initializing the db")
            raise ex

    def check_initialization_status(self):
        Logger.debug("Checking if initialized")
        is_file_present = os.path.exists(db_operations.constants.DB_PATH)
        if is_file_present:
            Logger.error("Initialization already performed")
            raise FileExistsError("DB File present")


