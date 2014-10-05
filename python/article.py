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
