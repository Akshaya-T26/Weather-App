import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the root directory
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """Backend Configuration using environment variables."""
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
    FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")

    @classmethod
    def validate(cls):
        """Validates configuration."""
        if not cls.OPENWEATHER_API_KEY or cls.OPENWEATHER_API_KEY == "your_api_key_here":
            # We don't raise error immediately to allow app to start,
            # but we should log/warn about it.
            return False
        return True
