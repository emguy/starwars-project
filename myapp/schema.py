import strawberry
import typing
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
  def persons(self, info: strawberry.types.Info) -> typing.List[Person]:
    return [ Person(name=obj['name'],
             films=obj['films'],
             vehicles=obj['vehicles'])
             for obj in handler.get_cached_result(
                info.variable_values['text']) ]


schema = strawberry.Schema(query=Query)
