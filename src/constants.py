# -*- coding: utf-8 -*-
"""
Repository: aspplicaton constants
"""


from enum import Enum

from fastapi import HTTPException

# DB_NAMING_CONVENTION = {
#     "ix": "%(column_0_label)s_idx",
#     "uq": "%(table_name)s_%(column_0_name)s_key",
#     "ck": "%(table_name)s_%(constraint_name)s_check",
#     "fk": "%(table_name)s_%(column_0_name)s_fkey",
#     "pk": "%(table_name)s_pkey",
# }

LOG_APP_NAME = "later"

class Environment(str, Enum):
    """Execution environment tracking"""

    LOCAL = "LOCAL"
    STAGING = "STAGING"
    TESTING = "TESTING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        """Local Dev environment"""
        return self in (self.LOCAL, self.STAGING, self.TESTING)

    @property
    def is_testing(self):
        """Pytest environment"""
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        """Is deployed to kubernetes"""
        return self in (self.STAGING, self.PRODUCTION)




class UserNotFoundException(Exception):
    """Raised when user is not found"""


class InvalidApiKeyException(HTTPException):
    """Raised when API keys are not found"""


class APIKeyNotFoundException(HTTPException):
    """Raised when API keys are not found"""
