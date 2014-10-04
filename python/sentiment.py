from multiprocessing import Pool
import urllib.request
import utils

GOOGLE_NEWS_RSS = "https://news.google.com/news/feeds?output=rss&q="
SPACE = "%20"
query = "iphone 6 bendgate"


query = query.replace(" ", "%20")
url = GOOGLE_NEWS_RSS+query
print(url)
response = str(urllib.request.urlopen(url).read())

# Get article links from the RSS
links = []
utils.find_links(links, response)
links = links[2:]

# Get article titles from the RSS
titles = []
utils.find_titles(titles, response)

num_links = len(links)
pool = Pool(processes=num_links)
sentiments, sentences = pool.map(utils.get_article_sentiment, links)

average_sentiment = utils.average_sentiment(sentiments, num_links)

result = {}
result["sentiment"] = average_sentiment
result["articles"] = []
for i in range(num_links):
    info = {}
    info["title"] = titles[i]
    info["link"] = links[i]
    info["sentiment"] = sentiments[i]
    result["articles"].append(info)
print(result)
