from boilerpipe.extract import Extractor
from idol_api import *


class ArticleExtractor(object):

	def extract(self, article):
		try:
			extractor = Extractor(extractor='ArticleSentencesExtractor', url=article.url)
		except Exception as e:
			return ''
		article_text = ''
		try:
			article_text = extractor.getText()
		except Exception:
			pass
		return article_text.encode('utf-8')


class EntityFinder(object):

	ENTITY_TYPES = ['companies_eng', 'organizations', 'universities', 'people_eng']
	MIN_SCORE = 0.03

	def entities(self, article, normalize=True):
		args = {'text': article.text, 'entity_type': EntityFinder.ENTITY_TYPES, 'show_alternatives': False}
		r = APIRequest(APIEndpoints.EXTRACT_ENTITIES, args).response()
		res = []
		for candidate in r['entities']:
			if candidate['score'] > EntityFinder.MIN_SCORE and candidate['original_text'] != 'too':
				res.append(candidate[('normalized_text' if normalize else 'original_text')])
		res = set(res)
		return res


class TokenFinder(object):

	MAX_TERMS = 50
	MAX_FILTERED_TERMS = 8
	MIN_WEIGHT = 100

	def tokens(self, article):
		args = {'text': article.text, 'stemming': False, 'max_terms': TokenFinder.MAX_TERMS}
		r = APIRequest(APIEndpoints.TOKENIZE_TEXT, args).response()
		candidates = []
		if 'terms' not in r:
			return set()
		for candidate in r['terms']:
			candidates.append(candidate)
		candidates.sort(key=lambda x: x['weight'])
		candidates = [candidate['term'] for candidate in reversed(candidates) if candidate['weight'] >= TokenFinder.MIN_WEIGHT]
		if len(candidates) >= TokenFinder.MAX_FILTERED_TERMS:
			return set(candidates[:TokenFinder.MAX_FILTERED_TERMS])
		else:
			return set(candidates)


class Article(object):

	MAX_SUMMARY_LEN = 120 # characters

	def __init__(self, url, title=''):
		self.url = url
		self.title = title
		self._extractor = ArticleExtractor()
		self._entity_finder = EntityFinder()
		self._token_finder = TokenFinder()
		self._text = None
		self._entities = None
		self._original_entities = None
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
	def original_entities(self):
		if not self._original_entities:
			self._original_entities = self._entity_finder.entities(self, False)
			return self._original_entities

	@property
	def tokens(self):
		if not self._tokens:
			self._tokens = self._token_finder.tokens(self)
		return self._tokens

	@property
	def all_entities(self):
		return self.tokens.union(self.entities)

	@property
	def all_original_entities(self):
		return set([item.lower() for item in list(self.tokens)]).union(self.original_entities)

	def _format_words(self, words):
		return [word.title() for word in words]

	@property
	def summary(self):
		summary = self.text
		if len(summary) < Article.MAX_SUMMARY_LEN:
			return summary
		elif summary.find('.') >= 0:
			i = summary.find('.')
			while i < self.MAX_SUMMARY_LEN * 0.75:
				i = summary.find('.', i + 1)
			return summary[:i+1]
		else:
			return summary[:Article.MAX_SUMMARY_LEN]

if __name__ == '__main__':
	a = Article('http://online.wsj.com/articles/book-review-how-google-works-by-eric-schmidt-and-jonathan-rosenberg-1412371982', 'blank')
	print a.summary
	print a.all_entities
	print a.all_original_entities
