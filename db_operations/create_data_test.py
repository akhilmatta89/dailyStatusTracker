import sqlite3
import unittest
from unittest.mock import patch

from db_operations import create_data
import exceptions.exceptions


class TestCreateData(unittest.TestCase):

    def setup(self):
        self.create = create_data.Create()

    def test_verify_req_body_when_wrong_request_body_should_throw_error(self):
        # Arrange
        self.setup()
        req_body = {
            "date": "2024-02-24",
            "day":"Monday",
            "task": ["Completed task-1", "start task-2"],
            "task_status": "Started"
        }
        # Act & Assert
        with self.assertRaises(exceptions.exceptions.InvalidRequestBody) as ex:
            self.create.verify_req_body(req_body)

        self.assertEqual(ex.exception.message, "Invalid Request Body: Either of keys is missing")

    def test_verify_req_body_when_correct_request_body_should_not_raise_error(self):
        # Arrange
        self.setup()
        req_body = {
            "date": "2024-02-24",
            "day":"Monday",
            "task": ["Completed task-1", "start task-2"],
            "task_status": "started",
            "remarks":""
        }
        # Act & Assert
        try:
            self.create.verify_req_body(req_body)
        except Exception:
            self.fail("Exception is not expected")

    @patch("sqlite3.connect")
    def test_add_status_into_db_when_success_should_not_throw_any_error(self, mock_connect):
        # Arrange
        self.setup()
        req_body = {
            "date": "2024-02-24",
            "day":"Monday",
            "task": ["Completed task-1", "start task-2"],
            "task_status": "started",
            "remarks":""
        }

        # Act
        try:
            self.create.add_status_into_db(req_body)
        # Assert
        except Exception:
            self.fail()

    def test_add_status_into_db_when_failure_should_throw_error(self):
        # Arrange
        self.setup()
        req_body = {
            "date": "2024-02-24",
            "day":"Monday",
            "task": ["Completed task-1", "start task-2"],
            "task_status": "started",
            "remarks":""
        }

        # Act & Assert
        with self.assertRaises(sqlite3.OperationalError) as ex:
            self.create.add_status_into_db(req_body)