class InvalidRequestBody(Exception):
    def __init__(self, error_message):
        message = f"Invalid Request Body: {error_message}"
        super().__init__(message)
        self.message = message

    def get_error_message(self):
        return self.message


class InvalidKey(Exception):
    def __init__(self, key):
        message = f"Invalid key passed: {key}"
        super().__init__(key)
        self.message = message

    def get_error_message(self):
        return self.message
