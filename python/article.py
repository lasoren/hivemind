from boilerpipe.extract import Extractor
import requests
import urllib
import json


class APIEndpoints(object):

	EXTRACT_ENTITIES = 'https://api.idolondemand.com/1/api/sync/extractentities/v1'


class DefaultAPIConfig(object):

	API_KEY = 'ef2c248e-a32d-47d2-836f-692976c55ead'


class APIRequest(object):

	def _process_args(self, args):
		filtered_args = {}
		extra_args = ''
		for argk, argv in args.items():
			if isinstance(argv, list):
				for v in argv:
					extra_args += argk + '=' + v + '&'
			else:
				filtered_args[argk] = argv
		args = urllib.urlencode(filtered_args) 
		if extra_args:
			args += '&' + extra_args[:-1]
		return args

	def __init__(self, url, args, config=DefaultAPIConfig):
		self.url = url
		if config.API_KEY:
			args['apikey'] = config.API_KEY
		self.args = self._process_args(args)

	def response(self):
		r = requests.get(self.url + '?' + self.args)
		return r.json()


class ArticleExtractor(object):

	@staticmethod
	def extract(article):
		extractor = Extractor(extractor='ArticleExtractor', url=article.url)
		article_text = ''
		try:
			article_text = extractor.getText()
		except Exception:
			pass
		return article_text


class EntityFinder(object):

	ENTITY_TYPES = ['companies_eng', 'organizations', 'universities', 'people_eng']
	
	@staticmethod
	def entities(article):
		args = {'text': article.text, 'entity_type': EntityFinder.ENTITY_TYPES, 'show_alternatives': True}
		r = APIRequest(APIEndpoints.EXTRACT_ENTITIES, args).response()
		candidates = r['entities']
		res = []
		for candidate in candidates:
			if candidate['score'] > 0.1:
				res.append(candidate['normalized_text'])
		res = set(res)
		return res


class Article(object):

	def __init__(self, url, title, extractor=ArticleExtractor, entity_finder=EntityFinder):
		self.url = url
		self.title = title
		self._extractor = extractor
		self._entity_finder = entity_finder
		self._text = None
		self._entities = None

	@property
	def text(self):
		if not self._text:
			self._text = self._extractor.extract(self)
		return self._text

	@property
	def entities(self):
		if not self._entities:
			self._entities = self._entity_finder.entities(self)
		return self._entities

print Article('http://www.christiantoday.com/article/iphone.6.problems.bendgate.still.continues.apple.mocked.videos.memes/41216.htm', 'blank').entities
