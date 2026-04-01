from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # gRPC
    grpc_port: int = 50051

    # Anthropic
    anthropic_api_key: str = ""

    # Model config
    auditor_model: str = "claude-sonnet-4-20250514"
    conclusion_model: str = "claude-sonnet-4-20250514"
    max_concurrent_auditors: int = 10

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
