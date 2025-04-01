from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from pydantic import AnyHttpUrl, field_validator, ValidationInfo

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

    @field_validator("SQLALCHEMY_DATABASE_URI", mode='before')
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> str:
        if isinstance(v, str):
            return v
        # Access other values via info.data
        return (
            f"postgresql+psycopg2://{info.data.get('POSTGRES_USER')}:{info.data.get('POSTGRES_PASSWORD')}"
            f"@{info.data.get('POSTGRES_SERVER')}:{info.data.get('POSTGRES_PORT')}/{info.data.get('POSTGRES_DB')}"
        )

    # Configure Pydantic BaseSettings
    model_config = SettingsConfigDict(
        case_sensitive=True, # Environment variables are typically case-sensitive
        env_file=".env"      # Specify the .env file to load
    )

# Create an instance of the settings
settings = Settings()