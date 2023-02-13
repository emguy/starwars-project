import base64
import flask
import json
import redis


# get the connection. the redis host is hard code.
def _get_connection():
  if not flask.has_app_context():
    return redis.Redis(host='0.0.0.0', port=6379, db=0)
  if not hasattr(flask.current_app, 'redis_pool'):
    flask.current_app.redis_pool = \
        redis.ConnectionPool(host='bell-redis', port=6379, db=0)
  return redis.Redis(connection_pool=flask.current_app.redis_pool)


# encode the cache key through base64
def _encode(text: str) -> str:
  return base64.b64encode(text.encode('utf-8')).decode('utf-8')


# put key-value pair into the cache
def put(key: str, val: object) -> bool:
  r = _get_connection()
  return r.set(_encode(key.strip()), json.dumps(val))


# get the value from the cache using the key
# return None if not found
def get(key: str):
  r = _get_connection()
  raw_value = r.get(_encode(key.strip()))
  if not raw_value:
    return None
  value = r.get(_encode(key.strip())).decode('utf-8')
  if value.startswith('[') and value.endswith(']'):
    return json.loads(value)
  if value.startswith('{') and value.endswith('}'):
    return json.loads(value)
  return value
