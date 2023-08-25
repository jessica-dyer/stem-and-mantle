import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/mylocaldb")
PORT = os.getenv("PORT", "Error: PORT has not been set.")
