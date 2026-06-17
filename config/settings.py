import os

from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

try:
    REQUEST_TIMEOUT = int(
        os.getenv("REQUEST_TIMEOUT", 10)
    )

    MAX_ARTICLES = int(
        os.getenv("MAX_ARTICLES", 25)
    )

except ValueError:
    raise ValueError("REQUEST_TIMEOUT and MAX_ARTICLES must be integers")


if not GNEWS_API_KEY:
    raise ValueError(
        "GNEWS_API_KEY not found in environment variables."
    )

if MAX_ARTICLES <= 0:
    raise ValueError("MAX_ARTICLES must be greater than 0.")

if REQUEST_TIMEOUT <= 0:
    raise ValueError("REQUEST_TIMEOUT must be greater than 0.")