import redis

user_redis = redis.StrictRedis.from_url('redis//localhost:6379')


class RUser(object):

	REDIS_EXPIRES = 7 * 24 * 60 * 60

	@classmethod
	def save_user_session(cls, user_uuid, openid, session_key):
		user_session_value = {
	        'openid': openid,
	        'session_key': session_key,
	        }
		user_session_key = user_uuid
		with user_redis.pipeline(transaction=False) as pipe:
			pipe.hmset(user_session_key, user_session_value)
			pipe.expire(user_session_key, cls.REDIS_EXPIRES)
			pipe.execute()
