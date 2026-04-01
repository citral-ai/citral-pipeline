from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "citral-pipeline"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://localhost:5432/citral"

    # Anthropic
    anthropic_api_key: str = ""

    # Cloudflare R2
    r2_endpoint: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_bucket_name: str = "citral-documents"

    # Clerk
    clerk_secret_key: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
