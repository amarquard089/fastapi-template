"""Settings for the application."""

from typing import Literal

from pydantic import BaseModel, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.utils.version import get_version


class App(BaseModel):
    """Application settings."""

    title: str = "FastAPI Template"
    summary: str = "An opinionated FastAPI template for building production-ready applications."
    description: str = (
        "An opinionated FastAPI template for building production-ready applications. "
        "Includes features like async SQLAlchemy, Alembic, and more."
    )

    @computed_field
    @property
    def version(self) -> str:
        """Determine the application version based on the environment."""
        return get_version()


class DB(BaseModel):
    """Database settings."""

    uri: str = Field(...)
    name: str = Field(...)
    user: str = Field(...)
    password: str = Field(...)

    @computed_field
    @property
    def async_url(self) -> str:
        """Construct the async database URL."""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.uri}/{self.name}"

    @computed_field
    @property
    def sync_url(self) -> str:
        """Construct the sync database URL."""
        return f"postgresql://{self.user}:{self.password}@{self.uri}/{self.name}"


class Settings(BaseSettings):
    """Settings for the application."""

    db: DB = Field(...)
    app: App = App()

    environment: Literal["development", "testing", "production"] = Field("development")

    @computed_field
    @property
    def is_production(self) -> bool:
        """Determine if the application is running in production."""
        return self.environment == "production"

    @computed_field
    @property
    def is_development(self) -> bool:
        """Determine if the application is running in development."""
        return self.environment == "development"

    @computed_field
    @property
    def is_testing(self) -> bool:
        """Determine if the application is running in testing."""
        return self.environment == "testing"

    @computed_field
    @property
    def log_level(self) -> str:
        """Determine the log level based on the environment."""
        if self.is_production:
            return "INFO"
        elif self.is_development:
            return "DEBUG"
        elif self.is_testing:
            return "WARNING"
        else:
            return "INFO"

    @computed_field
    @property
    def debug(self) -> bool:
        """Determine if the application is running in debug mode."""
        return self.is_development

    model_config = SettingsConfigDict(
        env_prefix="FASTAPI_TEMPLATE__",
        env_nested_delimiter="__",
        extra="ignore",
        env_file=".env",
    )


settings = Settings()
