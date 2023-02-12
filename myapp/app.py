from flask import Flask
from schema import schema
from strawberry.flask.views import GraphQLView
from werkzeug.exceptions import HTTPException
import requests


app = Flask(__name__)


# Production mode if False
app.config['TESTING'] = False


# Only a single endpoint is required for graphql
app.add_url_rule(
  "/myapp/graphql",
  view_func=GraphQLView.as_view("graphql_view", schema=schema),
)


# Here, we also inject CORS headers for UI development
@app.after_request
def add_headers_to_response(response):
  if app.config['TESTING']:
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = \
      'content-type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = \
      'OPTIONS, PUT, DELETE'
  return response


# Handle common exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    response = flask.make_response()
    response.content_type = "application/json"
    if isinstance(e, HTTPException):
      response.status_code = e.code
      response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
      })
    else:
      response.status_code = 500
      response.data = json.dumps({
        "code": 500,
        "name": 'internal error',
        "description": str(e),
      })
    return response


# Start the development server
if __name__ == "__main__":
  app.config['TESTING'] = True
  app.run(host='0.0.0.0', port=8000)
