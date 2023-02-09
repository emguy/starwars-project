from flask import Flask
from strawberry.flask.views import GraphQLView
from schema import schema
 
app = Flask(__name__)

app.add_url_rule(
  "/myapp/graphql",
  view_func=GraphQLView.as_view("graphql_view", schema=schema),
)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000)
