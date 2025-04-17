import time

from dataclasses import dataclass, field


@dataclass
class CryptoAPIException(Exception):
    code: str
    message: str
    timestamp: int = field(default_factory=lambda: int(time.time() * 1000))
    success: bool = False


@dataclass
class AuthenticationException(CryptoAPIException):
    code: str = "401"
    message: str = "Authentication failed"


@dataclass
class BadRequestException(CryptoAPIException):
    code: str = "400"
    message: str = "Bad Request"


@dataclass
class NotFoundException(CryptoAPIException):
    code: str = "404"
    message: str = "Not Found"


@dataclass
class RateLimitException(CryptoAPIException):
    code: str = "429"
    message: str = "Rate Limit Exceeded"


@dataclass
class InternalServerErrorException(CryptoAPIException):
    code: str = "500"
    message: str = "Internal Server Error"
