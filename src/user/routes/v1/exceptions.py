from typing import Any, Dict

from fastapi import HTTPException


class UserNotFound(HTTPException):
    def __init__(
        self,
        status_code: int = 404,
        detail: Any = "User not found",
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
