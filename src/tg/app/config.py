import os
from dotenv import load_dotenv

# load secrets
load_dotenv("secrets.env")

# global constants
TOKEN = os.getenv("TG_BOT_TOKEN", None)
# TOKEN = "7683833334:AAFhETifY8ClIWRm4xVUPn0GkHAWvdL2L1E"
