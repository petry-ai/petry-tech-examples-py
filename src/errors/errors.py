# Error when the wrong file format is uploaded
class InvalidFileFormatError(Exception):
    def __init__(self, expected_format: str):
        self.expected_format = expected_format
        self.message = f"Invalid file format. Expected {expected_format}'"
        super().__init__(self.message)
