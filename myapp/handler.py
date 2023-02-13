import cache
import json
import requests
import urllib.parse

SEARCH_ENDPOINT = 'https://swapi.dev/api/people?search={}'
PREFIX_SEARCH_TEXT = 'search%%'


# The following are the patterns that we use for caching
#
# 1 Search result, for example 'foobar'
#
#   base64('search%%foobar') => ['https://swapi.dev/api/people/6/',
#                                'https://swapi.dev/api/people/12/']
#
# 2 Entity data
#
#   base64('https://swapi.dev/api/people/6/') => '{the json data response}'
#   base64('https://swapi.dev/api/film/2/') => '{the json data response}'
#   base64('https://swapi.dev/api/vehicles/1/') => '{the json data response}'


# call the REST endpoint
def _call_api(url: str) -> object:
  r = requests.get(url, timeout=10)
  r.raise_for_status()
  return r.json()


# get the entity for people, film, or vehicles through its url
# call the remote endpoint only if it is not locally cached
def _get_entity(url: str) -> object:
  entity = cache.get(url)
  if not entity:
    entity = _call_api(url)
    cache.put(url, entity)
  return entity


# call the search endpoint and cache all the people entities
# from the response
def _search_remote_data(search_text: str) -> list:
  data = {'next': SEARCH_ENDPOINT.format(
         urllib.parse.quote(search_text.strip()))}
  person_list = []
  while data['next']:
    data = _call_api(data['next'])
    for obj in data['results']:
      cache.put(obj['url'], obj)
      person_list.append(obj['url'])
  cache.put(PREFIX_SEARCH_TEXT + search_text.strip(), person_list)
  return person_list


# this is the only exposed function. It attempts to load the search results
# from the local cache and builds the response data. It calls
# _search_remote_data only if the search result is not previously cached.
def get_cached_result(search_text: str) -> list:
  person_list = cache.get(PREFIX_SEARCH_TEXT + search_text.strip())
  if person_list is None:
    prev_list = cache.get(PREFIX_SEARCH_TEXT + search_text.strip()[0:-1])
    if prev_list is not None and len(prev_list) == 0:
      # we return empty list for 'foobar' without calling remote search api
      # provided that the cached result for 'fooba' is cached and is empty
      return []
    person_list = _search_remote_data(search_text)
  result_list = []
  for person_url in person_list:
    obj = _get_entity(person_url)
    result_list.append({
      'name': obj['name'],
      'films': [ _get_entity(url)['title'] for url in obj['films'] ],
      'vehicles': [ _get_entity(url)['model'] for url in obj['vehicles'] ],
    })
  return result_list
