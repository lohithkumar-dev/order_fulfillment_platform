from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = 'Order Fulfillment & Inventory Management Platform'
    DATABASE_URL: str = 'postgresql+psycopg://postgres:postgres@localhost:5432/order_fulfillment'
    SECRET_KEY: str = 'change-me-in-production'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = 'HS256'
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
