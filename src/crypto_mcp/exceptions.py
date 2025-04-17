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
    pass


@dataclass
class BadRequestException(CryptoAPIException):
    pass


@dataclass
class NotFoundException(CryptoAPIException):
    pass


@dataclass
class RateLimitException(CryptoAPIException):
    pass


@dataclass
class InternalServerErrorException(CryptoAPIException):
    pass
