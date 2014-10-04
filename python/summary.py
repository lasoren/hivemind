from boilerpipe.extract import Extractor
extractor = Extractor(extractor='ArticleExtractor', url='http://www.christiantoday.com/article/iphone.6.problems.bendgate.still.continues.apple.mocked.videos.memes/41216.htm')

print extractor.getText()