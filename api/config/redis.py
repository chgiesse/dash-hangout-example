import os
from dotenv import load_dotenv
from redis.asyncio import Redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError

load_dotenv()

ENVIRONMENT = os.environ.get("ENVIRONMENT")
SESSION_DB = 1
MAIN_DB = 0

retry = Retry(ExponentialBackoff(), 3)
main_redis_client = None
session_redis_client = None  # Added this back
sentinel_instance = None

if ENVIRONMENT == 'dev':
    REDIS_HOST = os.environ.get("REDIS_DEV_HOST")
    REDIS_PASSWORD = os.environ.get("REDIS_DEV_PASSWORD")
else:
    REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")


main_redis_client = Redis(
    host=REDIS_HOST,
    # password=REDIS_PASSWORD,
    db=MAIN_DB,
    retry=retry,
    retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError],
    decode_responses=True,
    max_connections=20,
)


session_redis_client = Redis(
    host=REDIS_HOST,
    password=REDIS_PASSWORD,
    db=SESSION_DB,  # Use session database
    retry=retry,
    retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError],
    max_connections=20,
)