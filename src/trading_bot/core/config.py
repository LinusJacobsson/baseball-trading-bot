from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    odds_api_key: str
    database_path: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
