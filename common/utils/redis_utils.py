from django.conf import settings
import redis,logging

logger = logging.getLogger("devops_platform_log")

class RedisBase(object):

    @staticmethod
    def getConnection(db=0):
        if settings.REDIS_POOL.get(db) == None:
            redis_connection = settings.REDIS_CONNECTION
            settings.REDIS_POOL[db] = redis.ConnectionPool(host=redis_connection['host'], port=redis_connection['port'],db=db)
        pools = settings.REDIS_POOL[db]
        connection = redis.Redis(connection_pool=pools)
        return connection

    @staticmethod
    def set(redisKey, value,time_ms=300,db=0):
        """
        在Redis中设置值，默认不存在则创建，存在则修改  过期时间默认300秒
        :param redisKey:
        :param value:
        :return:
        """
        redisConn = None
        try:
            redisConn = RedisBase.getConnection(db)
            # redisConn.set(redisKey, value)
            # redisConn.expire(redisKey, time_ms)
            redisConn.setex(redisKey,value,time_ms)
        except Exception as ex:
            logger.error(msg="Set redis key failed: {ex}".format(ex=str(ex)))
            return False
        finally:
            redisConn = None

    @staticmethod
    def get(redisKey,db=0):
        redisConn = None
        try:
            redisConn = RedisBase.getConnection(db)
            result = redisConn.get(redisKey)
            return result
        except Exception as ex:
            logger.error(msg="Get redis key failed: {ex}".format(ex=str(ex)))
            return False
        finally:
            redisConn = None

    @staticmethod
    def lpush(redisKey, data,db=0):
        redisConn = None
        try:
            redisConn = RedisBase.getConnection(db)
            redisConn.lpush(redisKey, data)
        except Exception as ex:
            logger.error(msg="Lpush data to redis failed: {ex}".format(ex=str(ex)))
            return False
        finally:
            redisConn = None

    @staticmethod
    def rpop(redisKey,db=0):
        redisConn = None
        try:
            redisConn = RedisBase.getConnection(db)
            data = redisConn.rpop(redisKey)
            return data
        except Exception as ex:
            logger.error(msg="Rpop redis key failed: {ex}".format(ex=str(ex)))
            return False
        finally:
            redisConn = None

    @staticmethod
    def llen(redisKey,db=0):
        redisConn = None
        try:
            redisConn = RedisBase.getConnection(db)
            return redisConn.llen(redisKey)
        except Exception as ex:
            logger.error(msg="Rpop redis key failed: {ex}".format(ex=str(ex)))
            return False
        finally:
            redisConn = None

    @staticmethod
    def lrange(redisKey,start=0,end=-1,db=0):
        redisConn = None
        try:
            redisConn = RedisBase.getConnection(db)
            return redisConn.lrange(redisKey,start,end)
        except Exception as ex:
            logger.error(msg="Rpop redis key failed: {ex}".format(ex=str(ex)))
            return False
        finally:
            redisConn = None

    @staticmethod
    def expire(key, time=600,db=0):
        """
        :param key:
        :param time: 秒
        :return:
        """
        redisConn = None
        try:
            redisConn = RedisBase.getConnection(db)
            return redisConn.expire(key,time)
        except Exception as e:
            logger.error(msg="Rpop redis key failed: {ex}".format(ex=str(ex)))
            return False
        finally:
            redisConn = None

    @staticmethod
    def exists(redisKey,db):
        redisConn = None
        try:
            redisConn = RedisBase.getConnection(db)
            return redisConn.exists(redisKey)
        except Exception as e:
            logger.error(msg="Rpop redis key failed: {ex}".format(ex=str(ex)))
            return False
        finally:
            redisConn = None

    @staticmethod
    def delete(redisKey,db=0):
        redisConn = None
        try:
            redisConn = RedisBase.getConnection(db)
            data = redisConn.delete(redisKey)
            return data
        except Exception as ex:
            logger.error(msg="Delete redis key failed: {ex}".format(ex=str(ex)))
            return False
        finally:
            redisConn = None

    @staticmethod
    def hset(redisKey, key, value, db=0):
        redisConn = None
        try:
            redisConn = RedisBase.getConnection(db)
            result = redisConn.hset(redisKey, key, value)
            return result
        except Exception as ex:
            logger.error(msg="hset redis key failed: {ex}".format(ex=str(ex)))
            return False
        finally:
            redisConn = None

    @staticmethod
    def hget(redisKey, key, db=0):
        redisConn = None
        try:
            redisConn = RedisBase.getConnection(db)
            result = redisConn.hget(redisKey, key)
            return result
        except Exception as ex:
            logger.error(msg="hget redis key failed: {ex}".format(ex=str(ex)))
            return False
        finally:
            redisConn = None

    @staticmethod
    def hgetAll(redisKey, db=0):
        redisConn = None
        try:
            redisConn = RedisBase.getConnection(db)
            result = redisConn.hgetall(redisKey)
            return result
        except Exception as ex:
            logger.error(msg="hgetAll redis key failed: {ex}".format(ex=str(ex)))
            return False
        finally:
            redisConn = None
