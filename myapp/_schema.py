import strawberry
import typing
import json
import handler


@strawberry.type
class Person:
  name: str
  films: typing.List[str]
  vehicles: typing.List[str]


@strawberry.type
class Query:
  @strawberry.field
  def search_text(self, text: str) -> str:
    return text

  @strawberry.field
#  def persons(self, info: strawberry.types.Info) -> typing.List[Person]:
  def persons(self) -> typing.List[Person]:
    return [ Person(name=obj['name'],
             films=obj['films'],
             vehicles=obj['vehicles'])
             for obj in handler.get_cached_result('La') ]
#                info.variable_values['text'])

schema = strawberry.Schema(query=Query)

if __name__ == '__main__':
#  query = '''
#  query MatchedPersons($text: String!) {
#    searchText(text: $text)
#    persons {
#      name
#      films
#      vehicles
#    }
#  }
#  '''
  query = '''
   {
    searchText(text: "La")
    persons (text: "La") {
      name
      films
      vehicles
    }
  }
  '''
  
  result = schema.execute_sync(query, variable_values={'text': 'La'})
  print(json.dumps(result.data))
