from boilerpipe.extract import Extractor


class ArticleSummarizer(object):
	@staticmethod
	def summarize(article):
		extractor = Extractor(extractor='ArticleExtractor', url=article.url)
		article_text = ''
		try:
			article_text = extractor.getText()
		catch Exception:
			pass
		return article_text

class EntityFinder(object):
	@staticmethod
	def entities(article):
		return []


class Article(object):
	def __init__(self, url, title, summarizer=ArticleSummarizer):
		self.url = url
		self.title = title
		self._summarizer = ArticleSummarizer

	@property
	def summary(self):
		if not self._summary:
			self._summary = self._summarizer.summarize(self)
		return self._summary

	def entities(self):
		if not self._entities:
			self._entities = self._entity_finder.entities(self)
		return self._entities