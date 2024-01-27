# -*- coding: utf-8 -*-
"""
Handle user authorization using JWT tokens
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

import database
from logger import logger
from src.models import basemodel

# from fastapi import Request, HTTPException
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# import certificate from certificates/private.key
JWT_SECRET: str = ""
JWT_ALGORITHM = "RS256"
if os.path.isfile("certificates/public.key"):
    with open("certificates/public.key", "r") as key_file:
        JWT_SECRET = str(key_file.read())
elif os.path.isfile("/code/certificates/public.key"):
    # for deployment in staging/prod
    with open("/code/certificates/public.key", "r") as key_file:
        JWT_SECRET = str(key_file.read())
else:
    raise FileNotFoundError("certificates/public.key not found")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: database.Session = Depends(database.get_db)
) -> database.User:
    """Dependency to verify JWt token and return user object"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        userid: str | None = payload.get("ID")
        subject: str | None = payload.get("Name")
        email: str | None = payload.get("Email")
        iss: str | None = payload.get("iss")
        if iss != "chefling":
            logger.error("JWTError: Invalid issuer:" + str(iss))
            raise credentials_exception

        # check expiry
        exp: int | None = payload.get("exp")
        if exp is None:
            logger.error("JWTError: Missing expiry")
            raise credentials_exception

        # check if token is expired
        if exp < int(time.time()):
            logger.error("JWTError: Token expired")
            raise credentials_exception

        if userid is None and email is None:
            logger.error("JWTError: Missing userid and email")
            raise credentials_exception
        token_data = basemodel.TokenData(userid=userid, subject=subject, email=email)

    except JWTError as exc:
        logger.error("JWTError: %s", exc)
        raise exc
    # Handle expired signature and return credential exception
    # @TODO: jose.exceptions.ExpiredSignatureError: Signature has expired.
    if token_data.userid is None:
        logger.error("JWTError: Missing userid")
        raise credentials_exception
    user = database.get_user(db, user_id=token_data.userid)
    if user is None:
        logger.error("JWTError: User not found")
        raise credentials_exception
    return user
