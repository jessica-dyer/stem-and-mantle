import os

DATABASE_URL = os.getenv("DATABASE_URL", "Error: DATABASE_URL is not set.")
PORT = os.getenv("PORT", "Error: PORT has not been set.")
