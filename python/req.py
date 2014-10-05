import requests
import urllib
import json

github_url = "https://api.idolondemand.com/1/api/sync/extractentities/v1"
entity_types = ['places_eng', 'companies_eng', 'organizations', 'universities', 'people_eng']
entity_types_str = ''
for entity_type in entity_types:
	entity_types_str += '&entity_type=' + entity_type
args = {'text': 'Barack Obama New Zealand', 'apikey': 'ef2c248e-a32d-47d2-836f-692976c55ead', 'show_alternatives': True}
data = urllib.urlencode(args) + entity_types_str

r = requests.get(github_url + '?' + data)


res = r.json()
print [entity['normalized_text'] for entity in res['entities'] if entity['score'] > 0.1]