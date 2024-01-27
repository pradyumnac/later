# -*- coding: utf-8 -*-
"""Handles all configurations for the app""" ""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Configuration for the app
    """

    # make environment variables case in-sensitive:
    # this is the default, specified to make it explicit
    # WARNING: .env should not be  checked in to git
    model_config = SettingsConfigDict(case_sensitive=False, env_nested_delimiter="__", env_file=".env")
    app_name: str = "cam_gateway"
    env: str = Field(default="dev")
    docs_enable: bool = Field(default=False)  # enable swagger/redoc
    debug: bool = Field(default=False)
    app_host: str = Field(default="0.0.0.0")
    app_port: str = Field(default="80")
    db_host: str = Field()
    db_port: int = Field()
    db_name: str = Field()
    db_user: str = Field()
    db_pwd: str = Field()

    def __init__(self):
        super().__init__()
        # print(f"Configuring {self.app_name} in {self.env} environment")
        if self.env == "dev":
            self.debug = True
            self.docs_enable = True
