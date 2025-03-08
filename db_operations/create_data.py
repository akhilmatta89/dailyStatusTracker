import sqlite3

import db_operations.constants
import exceptions.exceptions


class Create:

    def add_status_into_db(self, request_body):
        try:
            # query = db_operations.constants.ADD_STATUS_INTO_DB.format(Date=request_body.get("date"),
            #                                                           Day=request_body.get("day"),
            #                                                           Task=', '.join(request_body.get("task")),
            #                                                           Task_Status=request_body.get("task_status"),
            #                                                           Remarks = request_body.get("remarks"))
            query = '''
                INSERT INTO daily_status (Date, Day, Task, Task_Status, Remarks)
                VALUES (?, ?, ?, ?, ?)
                '''
            conn = sqlite3.connect(db_operations.constants.DB_PATH)

            cursor = conn.cursor()
            cursor.execute(query, (request_body.get("date"), request_body.get("day"), ', '.join(request_body.get("task")),
                                   request_body.get("task_status"), request_body.get("remarks")))
            conn.commit()
            conn.close()
        except Exception as ex:
            raise ex

    def verify_req_body(self, req_body):
        if len(req_body) != 5:
            raise exceptions.exceptions.InvalidRequestBody("Either of keys is missing")
        for key, value in req_body.items():
            if key not in db_operations.constants.CREATE_REQUEST_BODY_ITEMS:
                raise KeyError
            if key != "remarks" and value == "" or value == None:
                raise exceptions.exceptions.InvalidRequestBody("please provide valid values")
            if key == "task_status":
                if value.lower() not in db_operations.constants.TASK_STATUS_CONSTANTS:
                    raise exceptions.exceptions.InvalidRequestBody(f"task_status key values should be one among "
                                                                   f"{db_operations.constants.TASK_STATUS_CONSTANTS}")
