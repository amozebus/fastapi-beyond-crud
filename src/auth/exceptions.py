from fastapi import HTTPException, status


class BearerTokenException(HTTPException):
    def __init__(self, detail: str):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = detail
        self.headers = {"WWW-Authenticate": "Bearer"}
