import redis

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

EXPIRATION_TIME = 300

JWT_EXPIRATION_TIME = 1800