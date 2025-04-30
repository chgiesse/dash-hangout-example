from .config.redis import main_redis_client

import hashlib
import time
import orjson
from typing import Callable, Dict
from functools import wraps
from redis.asyncio import Sentinel
from redis.asyncio import Redis
from pandas import DataFrame

class RedisLruCache:

    def __init__(self, sentinels: Sentinel | Redis, service_name: str, max_size: int, env: str) -> None:
        self.sentinels = sentinels # sentinels is a plain redis client in development environment
        self.service_name = service_name
        self.max_size = max_size 
        self.env = env
        self.cache_key = "lru_cache:"
        self.access_order_key = "lru_cache_order:"


    def _hash_key(self, key: str):
        """Generate a consistent hash for the key"""
        return hashlib.md5(key.encode()).hexdigest()


    async def _get_master_connection(self):
        if self.env == 'dev':
            return self.sentinels
        return await self.sentinels.master_for(self.service_name)


    async def _get_slave_connection(self):
        if self.env == 'dev':
            return self.sentinels
        return await self.sentinels.slave_for(self.service_name)


    async def get(self, key: str):
        hashed_key = self._hash_key(key)
        slave = await self._get_slave_connection()
        value = await slave.hget(self.cache_key, hashed_key)
        if value:
            master = await self._get_master_connection()
            await master.zadd(self.access_order_key, {hashed_key: time.time()})
        return value


    async def set(self, key: str, value: any):
        hashed_key = self._hash_key(key)
        master = await self._get_master_connection()
        if await master.hset(self.cache_key, hashed_key, value):
            await master.zadd(self.access_order_key, {hashed_key: time.time()})
            await self._evict_if_needed(master)
        else:
            raise Exception('Failed to set value in cache')
    
    
    async def _evict_if_needed(self, master: Redis):
        current_size = await master.hlen(self.cache_key)
        if current_size > self.max_size:
            oldest_entry = await master.zrange(self.access_order_key, 0, 0)
            if oldest_entry:
                oldest_key = oldest_entry[0]
                await master.hdel(self.cache_key, oldest_key)
                await master.zrem(self.access_order_key, oldest_key)


    async def delete(self, key: str):
        hashed_key = self._hash_key(key) 
        master = await self._get_master_connection()
        await master.hdel(self.cache_key, hashed_key)
        await master.zrem (self.access_order_key, hashed_key)


    async def clear(self, namespace: str):
        master = await self._get_master_connection()

        ns_cache_key = self.cache_key + namespace
        ns_acces_order_key = self.access_order_key + namespace
        await master.delete(ns_cache_key)
        await master.delete(ns_acces_order_key)
    

    def cache(self, namespace: str, ttl: int | None = None):
        def decorator(func: Callable[[], DataFrame | Dict]):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # args[1:] -> exclude db session injection
                raw_key = f'{func.__name__}_' + hashlib.md5(str(args[1:] + tuple(kwargs.items())).encode()).hexdigest()
                cache_key = self._hash_key(raw_key)
                ns_cache_key = self.cache_key + namespace
                ns_access_order_key = self.access_order_key + namespace
                slave = await self._get_slave_connection()
                cached_result = await slave.hget(ns_cache_key, cache_key)
                if cached_result:
                    master = await self._get_master_connection()
                    await master.zadd(ns_access_order_key, {cache_key: time.time()})
                    decoded_result = orjson.loads(cached_result)
                    try:
                        columns = decoded_result['columns']
                        index = decoded_result['index']
                        data = decoded_result['data']
                        result_df = DataFrame(data, columns=columns, index=index)
                        return result_df
                    except:
                        pass
                    return decoded_result

                result = await func(*args, **kwargs)
                
                if result is not None:
                    if isinstance(result, DataFrame):
                        columns = list(result.columns)
                        index = list(result.index)
                        result_dict = result.to_dict(orient='records')
                        dump_obj = {
                            'data': result_dict,
                            'columns': columns,
                            'index': index
                        }
                        encoded_result = orjson.dumps(dump_obj)
                    else:
                        encoded_result = orjson.dumps(result)
                    
                    master = await self._get_master_connection()
                    await master.hset(ns_cache_key, cache_key, encoded_result)
                    await master.zadd(ns_access_order_key, {cache_key: time.time()})

                    if ttl is not None:
                        await master.expire(ns_cache_key, ttl)
                        await master.expire(ns_access_order_key, ttl)

                    await self._evict_if_needed(master)
                
                return result
            
            return wrapper
        
        return decorator
    
redis_lru_cache = RedisLruCache(main_redis_client, None, 100, 'dev')