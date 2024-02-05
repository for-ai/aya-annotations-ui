from fastapi import HTTPException

class InstructMultilingualAPIError(HTTPException):
    """
    Raised when an error occurs in the Instruct Multilingual API.
    """
    def __init__(self, detail, status_code):
        super().__init__(detail, status_code)
        self.detail = detail
        self.status_code = status_code


class DBIntegrityError(Exception):
    """
    Raised when a database integrity error occurs.
    """
    def __init__(self, message):
        super().__init__(message)


class IDNotFoundError(DBIntegrityError):
    """
    Raised when a specified ID is not found.
    """
    def __init__(self, message):
        super().__init__(message)
    
