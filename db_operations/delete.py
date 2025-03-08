import sqlite3

from db_operations import constants
from exceptions import exceptions


class DeleteData:

    def delete_data(self, date):
        try:
            query = constants.DELETE_STATUS_BASED_ON_DATE

            conn = sqlite3.connect(constants.DB_PATH)

            cursor = conn.cursor()
            cursor.execute(query, (date,))
            conn.commit()  # Required to apply deletion

            if cursor.rowcount == 0:
                raise exceptions.InvalidKey(date)
        except Exception as ex:
            raise ex
