from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Base for all application-level errors."""

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class NotFoundException(AppException):
    """Requested resource does not exist."""


class ConflictException(AppException):
    """Operation conflicts with existing state (e.g. duplicate email)."""


class BadRequestException(AppException):
    """Client input is invalid in a way Pydantic validation didn't catch."""


class UnauthorizedException(AppException):
    """Unauthorized Exception"""


class ForbiddenException(AppException):
    """Forbidden Exception"""


_STATUS_MAP: dict[type[AppException], int] = {
    NotFoundException: status.HTTP_404_NOT_FOUND,
    ConflictException: status.HTTP_409_CONFLICT,
    BadRequestException: status.HTTP_400_BAD_REQUEST,
    UnauthorizedException: status.HTTP_401_UNAUTHORIZED,
    ForbiddenException: status.HTTP_403_FORBIDDEN,
}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_execution_handler(request: Request, exc: AppException):
        code = _STATUS_MAP.get(type(exc), 500)
        return JSONResponse(status_code=code, content={"detail": exc.detail})
