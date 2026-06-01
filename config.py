from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


# DATABASE_URL : str = os.environ["DB_URL"]
# APP_ENV : str = os.getenv("APP_ENV", "DEV")


class Settings(BaseSettings):
    database_url: str
    app_env: str = "development"
    model_config = SettingsConfigDict(env_file=".env")
    jwt_expiry_minutes: int
    jwt_algorithm: str
    jwt_secret: str


settings = Settings()
