from pydantic import Field, PostgresDsn

from src.core.config import BaseSettings


class DatabaseSettings(BaseSettings):
    database_uri: PostgresDsn | str = "postgresql://postgres:qwerty@127.0.0.1:5432/test_project"

    @property
    def asyncpg_uri(self):
        s = str(self.database_uri)

        if "asyncpg" not in s:
            return s.replace("postgresql", "postgresql+asyncpg")

        return s
