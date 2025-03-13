import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY", "your_default_key_here")
    CRYPTO_API_URL = os.getenv("CRYPTO_API_URL", "https://api.coingecko.com/api/v3/simple/price")
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")  # Use Docker container name
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    QDRANT_HOST = os.getenv("QDRANT_HOST", "http://qdrant:6333")  # Container service name
    QDRANT_COLLECTION = "query_cache"

config = Config()
