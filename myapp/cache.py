import json
import redis
import flask

def get_connection():
  if flask.has_app_context():
    if 'redis_pool' not in flask.current_app:
        flask.current_app.redis_pool = redis.ConnectionPool(host='0.0.0.0', port=6379, db=0)
    return redis.Redis(flask.current_app.redis_pool)
  return redis.Redis(host='0.0.0.0', port=6379, db=0)

def put(key, val) -> bool:
  r = get_connection()
  return r.set(key, val)

def get(key) -> str:
  r = get_connection()
  value = r.get(key).decode('utf-8')
  if value.startswith('[') and value.endswith(']'):
    return json.loads[value]
  if value.startswith('{') and value.endswith('}'):
    return json.loads[value]
  return value
