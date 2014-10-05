from boilerpipe.extract import Extractor
from idol_api import *


class ArticleExtractor(object):

	def extract(self, article):
		try:
			extractor = Extractor(extractor='ArticleSentencesExtractor', url=article.url)
		except Exception as e:
			return e.msg
		article_text = ''
		try:
			article_text = extractor.getText()
		except Exception:
			pass
		return article_text.encode('utf-8')


class EntityFinder(object):

	ENTITY_TYPES = ['companies_eng', 'organizations', 'universities', 'people_eng']
	MIN_SCORE = 0.1
	
	def entities(self, article):
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

	def tokens(self, article):
		args = {'text': article.text, 'stemming': False, 'max_terms': TokenFinder.MAX_TERMS}
		r = APIRequest(APIEndpoints.TOKENIZE_TEXT, args).response()
		candidates = []
		for candidate in r['terms']:
			candidates.append(candidate)
		candidates.sort(key=lambda x: x['weight'])
		candidates = [candidate['term'] for candidate in reversed(candidates) if candidate['weight'] >= 100]
		if len(candidates) >= TokenFinder.MAX_FILTERED_TERMS:
			return set(candidates[:TokenFinder.MAX_FILTERED_TERMS])
		else:
			return set(candidates)


class Article(object):

	MAX_SUMMARY_LEN = 150 # characters

	def __init__(self, url, title=''):
		self.url = url
		self.title = title
		self._extractor = ArticleExtractor()
		self._entity_finder = EntityFinder()
		self._token_finder = TokenFinder()
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

	@property
	def summary(self):
		summary = self.text
		if len(summary) < Article.MAX_SUMMARY_LEN:
			return summary
		elif summary.find('.') >= 0:
			return summary[:summary.find('.')+1]
		else:
			return summary[:Article.MAX_SUMMARY_LEN]

if __name__ == '__main__':
	a = Article('http://www.csmonitor.com/USA/2014/1004/Many-Ebola-inquiries-around-the-US-but-just-one-confirmed-case-so-far-video', 'blank')
	print a.summary
	print a.all_entities
