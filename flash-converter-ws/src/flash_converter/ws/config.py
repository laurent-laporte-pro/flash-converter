"""
Web service configuration
"""

import logging
import typing as t

from flash_converter_wf.config import Settings as CommonSettings
from pydantic import BeforeValidator

SENSITIVE_KEYS = {
    # Authentication & Authorization
    "PASSWORD",
    "SECRET",
    "SECRET_KEY",
    "PRIVATE_KEY",
    "API_KEY",
    "API_SECRET",
    "ACCESS_TOKEN",
    "REFRESH_TOKEN",
    "AUTH_TOKEN",
    "JWT_SECRET",
    "OAUTH_TOKEN",
    "SESSION_KEY",
    "SECURITY_KEY",
    # Database
    "DB_PASSWORD",
    "DATABASE_PASSWORD",
    "DB_USERNAME",
    "DATABASE_URL",
    "POSTGRES_PASSWORD",
    "MYSQL_PASSWORD",
    "MONGODB_PASSWORD",
    "REDIS_PASSWORD",
    # Cloud services & APIs
    "AWS_SECRET_ACCESS_KEY",
    "AWS_ACCESS_KEY_ID",
    "AZURE_CLIENT_SECRET",
    "GCP_PRIVATE_KEY",
    "GITHUB_TOKEN",
    "STRIPE_SECRET_KEY",
    "PAYPAL_SECRET",
    "SENDGRID_API_KEY",
    "TWILIO_AUTH_TOKEN",
    # Certificates & Keys
    "SSL_KEY",
    "SSL_CERT",
    "SSH_PRIVATE_KEY",
    "SIGNING_KEY",
    "ENCRYPTION_KEY",
    # Identity providers
    "CLIENT_SECRET",
    "CLIENT_ID",
    "ADMIN_PASSWORD",
    "ROOT_PASSWORD",
    "MASTER_KEY",
    # Email
    "EMAIL_PASSWORD",
    "SMTP_PASSWORD",
    "MAIL_PASSWORD",
    # Webhooks
    "WEBHOOK_SECRET",
    "WEBHOOK_TOKEN",
    # 2FA/MFA
    "MFA_SECRET",
    "TOTP_KEY",
    "2FA_SECRET",
    # Common sensitive keys
    *[f"{key}_DEV" for key in ("SECRET", "PASSWORD", "KEY")],
    *[f"{key}_PROD" for key in ("SECRET", "PASSWORD", "KEY")],
    *[f"{key}_TEST" for key in ("SECRET", "PASSWORD", "KEY")],
    *[f"{key}_STAGING" for key in ("SECRET", "PASSWORD", "KEY")],
}


def _normalize_origins(origins: str) -> str:
    """Normalize the origins by removing whitespace and trailing slashes."""
    origins = origins.strip()
    origin_urls = {o.strip() for o in origins.split(",")} if origins else set()
    return ",".join(str(o).rstrip("/") for o in origin_urls)


AllowOrigins = t.Annotated[str, BeforeValidator(_normalize_origins)]


class Settings(CommonSettings):
    """
    Web service configuration
    """

    # The FastAPI application uses the Celery application,
    # so the FastAPI settings should inherit the Celery settings
    # and extend them with the FastAPI-specific settings.

    # Configuration of the CORS middleware
    ALLOW_ORIGINS: AllowOrigins = "http://localhost:5173, http://127.0.0.1:5173"

    def display_settings(self, logger: logging.Logger | None = None) -> None:
        """
        Display the settings in the log.
        """
        logging_config = self.model_dump(mode="json")
        logging_config = {k: ("********" if k in SENSITIVE_KEYS else v) for k, v in logging_config.items()}
        logger.info("------- Actual settings -------")
        for name, value in logging_config.items():
            logger.info("- %s: %r", name, value)
        logger.info("-------------------------------")


settings = Settings()
