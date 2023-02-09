import strawberry
import requests
import typing
import json

PERSON_SEARCH_ENDPOINT = "https://swapi.dev/api/people?search="

PERSON_CACHE = {
  "Foo barA": {
    "films": [
      "film1",
      "film2",
      "film3",
    ],
    "vehicles": [
     ]
  },
  "Foo barB": {
    "films": [
      "film1",
      "film2",
      "film3",
    ]
  }
}

@strawberry.type
class Person:
  name: str

  @strawberry.field
  def films(self) -> typing.List[str]:
    return [_title for _title in PERSON_CACHE[self.name]['films']]


@strawberry.type
class Query:
  @strawberry.field
  def name(self, text: str) -> str:
    return text

  @strawberry.field
  def persons(self) -> typing.List[Person]:
    return [Person(name=_name) for _name in PERSON_CACHE.keys()] 

schema = strawberry.Schema(query=Query)

if __name__ == '__main__':
  query = '''
  {
    name(text:"foo")
    persons {
      name
      films
    }
  }
  '''
  
  result = schema.execute_sync(query)
  print(json.dumps(result.data))
