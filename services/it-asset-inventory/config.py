import os

# it-asset-inventory settings, read from the environment
DB_HOST = os.environ.get("DB_HOST", "")
DB_PORT = int(os.environ.get("DB_PORT", "1433"))
DB_NAME = os.environ.get("DB_NAME", "ITAM")
DB_USER = os.environ.get("DB_USER", "")
DB_PASSWORD_SECRET_NAME = os.environ.get("DB_PASSWORD_SECRET_NAME", "dts/it-asset-inventory/db")

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

PORT = int(os.environ.get("PORT", "8080"))
