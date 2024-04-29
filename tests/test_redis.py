import redis

redis_client = redis.Redis(host='172.232.237.13', port=6011, db=0)

try:
    redis_client.ping()
    print("Redis is connected!")
except redis.ConnectionError:
    print("Redis is not connected")
