from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    database_url: str
    rabbitmq_url: str

    model_config = {
        "env_file": ".env.test" if os.getenv("TESTING") else ".env"
    }


settings = Settings()
