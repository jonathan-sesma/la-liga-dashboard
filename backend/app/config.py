import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "La Liga Dashboard"

    VERSION: str = "1.0.0"

    FOOTBALL_API_KEY: str = os.getenv("FOOTBALL_API_KEY")

    FOOTBALL_API_URL: str = os.getenv("FOOTBALL_API_URL")

    def __init__(self):
        if not self.FOOTBALL_API_KEY:
            raise ValueError("FOOTBALL_API_KEY is not set in environment variables")

settings = Settings()