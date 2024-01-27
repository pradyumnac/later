# -*- coding: utf-8 -*-
"""
All Pydantic models are defined in this folder
- request models
- response models
- cross module models
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

import constants


class Token(BaseModel):
    """
    Pydanctic models for JWT token
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Pydanctic models for JWT token data contents - subject, id, email
    """

    userid: int | None
    email: str | None
    subject: str | None


class TokenUser(BaseModel):
    """Chefling Auth user model"""

    userid: int
    email: str | None

class LaterFilter(BaseModel):
    """Laterfilter model"""

    later_type: constants.LaterType | None = None
    status: constants.LaterStatus | None = None
    sort: constants.Sort | None = None
    page: int | None = None
    limit: int | None = None

class User(BaseModel):
    """User model"""

    id: int
    email: str
    username: str
    created_at: datetime
    updated_at: datetime
    is_superuser: bool

class UserSubscriptions(BaseModel):
    """User subscriptionmodel"""

    id: int
    email: str
    username: str
    validity_start: datetime
    validity_end: datetime
    created_at: datetime
    updated_at: datetime
    status: constants.SubscriptionStatus