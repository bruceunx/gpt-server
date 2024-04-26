import redis

redis_client = redis.Redis(host='', port=000, db=0, password="")

try:
    redis_client.ping()
    print("Redis is connected!")
except redis.ConnectionError:
    print("Redis is not connected")
