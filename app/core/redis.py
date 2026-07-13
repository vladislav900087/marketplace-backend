import redis

redis_client = redis.Redis(host='redis://red-d9ai54ok1i2s73c5pev0:6379', port=6379, decode_responses=True)

EXPIRATION_TIME = 300

JWT_EXPIRATION_TIME = 1800