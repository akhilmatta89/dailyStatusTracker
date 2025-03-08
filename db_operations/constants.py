"""
DataBase Queries
"""

CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS daily_status (
                            Date TEXT UNIQUE,
                            Day TEXT NOT NULL,
                            Task TEXT NOT NULL,
                            Task_Status TEXT NOT NULL,
                            Remarks TEXT)'''

ADD_STATUS_INTO_DB = '''INSERT INTO daily_status (Date, Day, Task, Task_Status, Remarks) VALUES {Date}, {Day}, 
{Task}, {Task_Status}, {Remarks} '''

SELECT_ALL_STATUS = '''SELECT * FROM daily_status'''

SELECT_STATUS_BASED_ON_DATE = '''SELECT * FROM daily_status WHERE date = ?'''

DELETE_STATUS_BASED_ON_DATE = '''DELETE FROM daily_status where date=?'''

"""
DataBase Related Constants
"""
DB_PATH = "./instance/student_status.db"
CREATE_REQUEST_BODY_ITEMS = ["date", "day", "task", "task_status", "remarks"]
TASK_STATUS_CONSTANTS = ["yet to start", "started", "in progess", "on hold", "completed"]