from boilerpipe.extract import Extractor
from idol_api import *


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
	MIN_SCORE = 0.1
	
	@staticmethod
	def entities(article):
		args = {'text': article.text, 'entity_type': EntityFinder.ENTITY_TYPES, 'show_alternatives': True}
		r = APIRequest(APIEndpoints.EXTRACT_ENTITIES, args).response()
		res = []
		for candidate in r['entities']:
			if candidate['score'] > EntityFinder.MIN_SCORE:
				res.append(candidate['normalized_text'])
		res = set(res)
		return res


class TokenFinder(object):

	MAX_TERMS = 50
	MAX_FILTERED_TERMS = 8

	@staticmethod
	def tokens(article):
		args = {'text': article.text, 'stemming': False, 'max_terms': TokenFinder.MAX_TERMS}
		r = APIRequest(APIEndpoints.TOKENIZE_TEXT, args).response()
		candidates = []
		for candidate in r['terms']:
			candidates.append(candidate)
		candidates.sort(key=lambda x: x['weight'])
		print candidates
		candidates = [candidate['term'] for candidate in reversed(candidates) if candidate['weight'] >= 100]
		if len(candidates) >= TokenFinder.MAX_FILTERED_TERMS:
			return set(candidates[:TokenFinder.MAX_FILTERED_TERMS])
		else:
			return set(candidates)


class Article(object):

	def __init__(self, url, title, extractor=ArticleExtractor, entity_finder=EntityFinder, token_finder=TokenFinder):
		self.url = url
		self.title = title
		self._extractor = extractor
		self._entity_finder = entity_finder
		self._token_finder = token_finder
		self._text = None
		self._entities = None
		self._tokens = None

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

	@property
	def tokens(self):
		if not self._tokens:
			self._tokens = self._token_finder.tokens(self)
		return self._tokens

	@property
	def all_entities(self):
		return self._format_words(self.tokens.union(self.entities))

	def _format_words(self, words):
		return [word.title() for word in words]

print Article('http://www.christiantoday.com/article/iphone.6.problems.bendgate.still.continues.apple.mocked.videos.memes/41216.htm', 'blank').all_entities
