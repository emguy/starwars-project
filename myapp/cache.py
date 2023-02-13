import base64
import flask
import json
import redis


def get_connection():
  if not flask.has_app_context():
    return redis.Redis(host='0.0.0.0', port=6379, db=0)
  if not hasattr(flask.current_app, 'redis_pool'):
    flask.current_app.redis_pool = \
        redis.ConnectionPool(host='bell-redis', port=6379, db=0)
  return redis.Redis(connection_pool=flask.current_app.redis_pool)


def _encode(text: str) -> str:
  return base64.b64encode(text.encode('utf-8')).decode('utf-8')


def put(key: str, val: object) -> bool:
  r = get_connection()
  return r.set(_encode(key.strip()), json.dumps(val))


def get(key: str):
  r = get_connection()
  raw_value = r.get(_encode(key.strip()))
  if not raw_value:
    return None
  value = r.get(_encode(key.strip())).decode('utf-8')
  if value.startswith('[') and value.endswith(']'):
    return json.loads(value)
  if value.startswith('{') and value.endswith('}'):
    return json.loads(value)
  return value
