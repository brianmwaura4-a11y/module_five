import os

from dotenv import load_dotenv

load_dotenv()  # Pulls variables from a .env file into the environment


class BaseConfig:
    """Default settings shared by all environments."""
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "default-secret-key")
    JSON_SORT_KEYS: bool = False          # Keeps JSON key order stable in Flask
    DATABASE_PATH: str = os.environ.get("DATABASE_PATH", "hrms.db")
    CORS_ALLOWED_ORIGIN: str = os.environ.get("CORS_ALLOWED_ORIGIN", "*")
    SEED_DATA: bool = False               # Whether to insert dummy data on startup
    DEFAULT_PAGE_SIZE: int = 20           # Pagination fallback


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    ENV: str = "development"
    SEED_DATA: bool = True


class TestingConfig(BaseConfig):
    TESTING: bool = True
    DEBUG: bool = True
    ENV: str = "testing"
    SEED_DATA: bool = True
    WTF_CSRF_ENABLED: bool = False        # Disable CSRF for easier API testing
    DATABASE_PATH: str = os.environ.get("DATABASE_PATH", ":memory:")


class ProductionConfig(BaseConfig):
    DEBUG: bool = False
    ENV: str = "production"
    SEED_DATA: bool = False
    # Force the operator to supply a real secret in production
    SECRET_KEY: str = os.environ.get("SECRET_KEY")  # type: ignore[assignment]


# Map string names to config classes so create_app() can pick one.
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
