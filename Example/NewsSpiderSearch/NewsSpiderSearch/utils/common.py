import pickle

import redis

__author__ = 'action'


redis_cli = redis.StrictRedis()




def real_time_count(key, init):
    if redis_cli.get(key):
        count = pickle.loads(redis_cli.get(key))
        count = count + 1
        count = pickle.dumps(count)
        redis_cli.set(key, count)
    else:
        count = pickle.dumps(init)
        redis_cli.set(key, count)


