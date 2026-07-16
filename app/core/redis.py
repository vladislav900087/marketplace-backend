import os
import redis


redis_url = os.getenv('REDIS_URL')
redis_client = redis.from_url(redis_url)

EXPIRATION_TIME = 300

JWT_EXPIRATION_TIME = 1800