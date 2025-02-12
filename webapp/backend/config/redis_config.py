import os
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Redis connection
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=int(os.getenv("REDIS_DB")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,  # Ensures data is returned as strings
)