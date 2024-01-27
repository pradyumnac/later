# -*- coding: utf-8 -*-
"""
Request Pydantic models for API Service
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# The entire service will be prefixed with /api/v1/camgateway
from datetime import datetime

from pydantic import BaseModel

import constants
from src.models.basemodel import User, LaterFilter

class RegisterUser(BaseModel):
    """RegisterUser model"""

    email: str
    phone: str
    password: str
    username: str

class LoginUser(BaseModel):
    """LoginUser model"""

    email: str
    password: str

class ResetPassword(BaseModel):
    """ResetPassword model"""

    email: str
    password: str
    token: str

class ResetPasswordRequest(BaseModel):
    """ResetPasswordRequest model"""

    email: str

class UpdateProfile(BaseModel):
    """UpdateProfile model"""

    email: str | None = None
    phone: str | None = None
    username: str | None = None
    password: str | None = None

class GetLaterList(BaseModel):
    """GetLaterList model"""

    filter: LaterFilter



class AddForLater(BaseModel):
    """AddForLater model"""

    id: int
    