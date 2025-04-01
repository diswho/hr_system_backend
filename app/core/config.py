from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    # Define your settings fields here, matching the .env variables
    # Pydantic automatically reads environment variables (case-insensitive)
    # or variables from a .env file

    # Project Settings
    PROJECT_NAME: str = "HR System API"
    API_V1_STR: str = "/api/v1" # Example prefix for API versioning

    # Security Settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # BACKEND_CORS_ORIGINS is a list of strings, Pydantic can parse it
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Allow parsing CORS origins from a string separated by commas
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            # Split the string by commas and strip whitespace
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # First Superuser (Example for initial setup)
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    # Database Settings (Example for PostgreSQL)
    POSTGRES_SERVER: str
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    # Construct database URL (adjust if using a different DB)
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return (
            f"postgresql+psycopg2://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}"
            f"@{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}"
        )

    # Configure Pydantic BaseSettings
    model_config = SettingsConfigDict(
        case_sensitive=True, # Environment variables are typically case-sensitive
        env_file=".env"      # Specify the .env file to load
    )

# Create an instance of the settings
settings = Settings()