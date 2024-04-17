from enum import Enum

from src.core.config.base import BaseSettings
from src.core.config.database import DatabaseSettings
from src.core.config.log import LogSettings
from src.core.config.server import ServerSettings


class ApplicationEnvironment(str, Enum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"
    TEST = "test"


class ApplicationSettings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    log: LogSettings = LogSettings()
    server: ServerSettings = ServerSettings()


settings = ApplicationSettings()
