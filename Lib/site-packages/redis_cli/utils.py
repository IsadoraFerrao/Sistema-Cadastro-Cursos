import redis

from redis_cli.client import RedisWrapper


def get_redis():
    return RedisWrapper.get_redis()


def init_from_redis(redis_instance: redis.Redis):
    return RedisWrapper.init_from_redis(redis_instance)


def init_from_sentinel(sentinel_instance: redis.Sentinel, service_name, **kwargs):
    return RedisWrapper.init_from_sentinel(sentinel_instance, service_name, **kwargs)
