# -*- coding: utf-8 -*-
"""
Response Pydantic models for API Service
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# The entire service will be prefixed with /api/v1/camgateway
from datetime import datetime
from typing import List

from pydantic import BaseModel

import constants
from src.models.basemodel import Device, DeviceEvent, DeviceState, Job

# Response Models


class ResponseModel(BaseModel):
    """Pydantic models for enforcing response params"""

    status: int
    message: str

