import urllib.request
import utils

ef2c248e-a32d-47d2-836f-692976c55ead

GOOGLE_NEWS_RSS = "https://news.google.com/news/feeds?output=rss&q="
SPACE = "%20"
query = "iphone 6 bendgate"


query = query.replace(" ", "%20")
url = GOOGLE_NEWS_RSS+query
print(url)
response = str(urllib.request.urlopen(url).read())

links = []
utils.find_links(links, response)
print(links)

