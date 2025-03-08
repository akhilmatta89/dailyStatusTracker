import sqlite3
import db_operations.constants
import exceptions.exceptions


class GetData:

    def get_all_data(self):
        task_data = []
        try:
            query = db_operations.constants.SELECT_ALL_STATUS
            conn = sqlite3.connect(db_operations.constants.DB_PATH)

            cursor = conn.cursor()
            cursor.execute(query)
            # Fetch the records
            records = cursor.fetchall()  # Use fetchall() if you expect multiple rows

            # Close the connection
            conn.close()

            # If data exists, return it as JSON, otherwise return an error message
            if records:
                for each_record in records:
                    # Format the records into a dictionary
                    task_data_each = {
                        "date": each_record[0],
                        "day": each_record[1],
                        "task": each_record[2],
                        "task_status": each_record[3],
                        "remarks": each_record[4]
                    }
                    task_data.append(task_data_each)
            return task_data
        except Exception as ex:
            raise ex

    def get_data(self, date):
        try:
            query = db_operations.constants.SELECT_STATUS_BASED_ON_DATE
            conn = sqlite3.connect(db_operations.constants.DB_PATH)

            cursor = conn.cursor()
            cursor.execute(query, (date,))
            # Fetch the records
            records = cursor.fetchone()  # Use fetchall() if you expect multiple rows

            # Close the connection
            conn.close()

            # If data exists, return it as JSON, otherwise return an error message
            if records:
                # Format the records into a dictionary
                task_data_each = {
                    "date": records[0],
                    "day": records[1],
                    "task": records[2].split(","),
                    "task_status": records[3],
                    "remarks": records[4]
                }
                return task_data_each
            else:
                raise exceptions.exceptions.InvalidKey(date)
        except Exception as ex:
            raise ex


