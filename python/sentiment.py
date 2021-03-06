from thread_pool import ThreadPool
import requests
import utils

GOOGLE_NEWS_RSS = "https://news.google.com/news/feeds?output=rss&q="
SPACE = "%20"
query = "Snuggie"

query = query.replace(" ", "%20")
url = GOOGLE_NEWS_RSS+query
response = requests.get(url).text

# Get article links from the RSS
links = []
utils.find_links(links, response)
if len(links) > 2:
    links = links[2:]

# Get article titles from the RSS
titles = []
utils.find_titles(titles, response)
if len(titles) > 2:
    titles = titles[2:]

num_links = len(links)
num_titles = len(titles)
if num_titles < num_links:
    links = links[:num_titles]
if num_links < num_titles:
    titles = titles[:num_links]

articles = {}
pool = ThreadPool(num_links)
for i in range(num_links):
    pool.add_task(
        utils.get_article_sentiment, links[i], titles[i], articles)
pool.wait_completion()

sentiments = []

result = {}
result["articles"] = []
for key in articles:
    info = {}
    info["title"] = articles[key]["title"]
    info["link"] = key
    sentiments.append(articles[key]["sentiment"])
    info["sentiment"] = articles[key]["sentiment"]
    info["snippet"] = articles[key]["snippet"]
    result["articles"].append(info)

average_sentiment = utils.average_sentiment(
    sentiments,
    len(sentiments))
result["sentiment"] = average_sentiment
print(result)
