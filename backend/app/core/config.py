import os

from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv(dotenv_path="F:/TitanForge/backend/.env")


class Settings:
    """
    Configuration settings for the TitanForge application.
    Reads values from environment variables.
    """

    # LLM Configuration
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "mock-response")

    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://titan:forge@localhost:5432/titanforge"
    )

    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # Stripe Configuration
    STRIPE_API_KEY: str | None = os.getenv("STRIPE_API_KEY")
    STRIPE_WEBHOOK_SECRET: str | None = os.getenv("STRIPE_WEBHOOK_SECRET")

    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "your-super-secret-key"
    )  # IMPORTANT: Change this in production!

    # Social Media Configuration
    FACEBOOK_ACCESS_TOKEN: str | None = os.getenv(
        "FACEBOOK_USER_TOKEN"
    )  # Using USER_TOKEN from provided env
    LINKEDIN_ACCESS_TOKEN: str | None = os.getenv("LINKEDIN_ACCESS_TOKEN")

    # Email Configuration (SMTP)
    SMTP_HOST: str | None = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 465))
    SMTP_USER: str | None = os.getenv("SMTP_USER")
    SMTP_PASSWORD: str | None = os.getenv("SMTP_PASS")

    # WordPress Blog Configuration
    WORDPRESS_API_URL: str | None = os.getenv(
        "WORDPRESS_API_URL"
    )  # This should be the REST API endpoint
    WORDPRESS_USER: str | None = os.getenv("WORDPRESS_USER")
    WORDPRESS_PASSWORD: str | None = os.getenv(
        "WORDPRESS_PASSWORD"
    )  # Or APP specific password

    # Shopify Configuration
    SHOPIFY_SHOP_URL: str | None = os.getenv("SHOPIFY_SHOP_URL")
    SHOPIFY_API_VERSION: str = os.getenv(
        "SHOPIFY_API_VERSION", "2024-01"
    )  # Default to a recent stable API version
    SHOPIFY_ADMIN_API_TOKEN: str | None = os.getenv(
        "SHOPIFY_ADMIN_ACCESS_TOKEN"
    )  # Often called Admin API Access Token


settings = Settings()
