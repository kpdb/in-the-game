import os
from arq.connections import RedisSettings

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

settings = RedisSettings(host=REDIS_HOST, port=REDIS_PORT)
