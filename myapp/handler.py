import cache
import json
import requests
import urllib.parse

SEARCH_ENDPOINT = 'https://swapi.dev/api/people?search={}'
PREFIX_SEARCH_TEXT = 'search%%'


def _call_api(url: str) -> object:
  r = requests.get(url, timeout=3)
  r.raise_for_status()
  return r.json()

def _get_entity(url: str) -> object:
  entity = cache.get(url)
  if not entity:
    entity = _call_api(url)
    cache.put(url, entity)
  return entity

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

def get_cached_result(search_text: str) -> list:
  person_list = cache.get(PREFIX_SEARCH_TEXT + search_text.strip())
  if not person_list:
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
