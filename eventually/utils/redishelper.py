"""
Redis helper
=============
The module that provides functionality for setting and getting records to redis.
"""
import redis


class RedisWorker():
    """The class that provide api for redis interaction"""
    instance = None
    redis = redis.Redis()

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(RedisWorker, cls).__new__(cls)
        return cls.instance

    def set(self, key, value):
        """Function that set records to redis db"""
        self.redis.set(key, value)
        self.redis.expire(key, 50)
        return True

    def get(self, key):
        """Function that get records from redis db"""
        return self.redis.get(key)

redisHelper = RedisWorker()
