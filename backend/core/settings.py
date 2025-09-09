import os

class Settings:
    def __init__(self):
        self.api_base: str = "/api"
        self.port: int = 8080
        self.algorithm: str = "HS256"
        self.access_token_expire_minutes: int = 30
        self.app_version = os.getenv("APP_VERSION")
        self.database_url = os.getenv('DATABASE_URL')
        self.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

settings = Settings()
