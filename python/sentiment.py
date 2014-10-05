from thread_pool import ThreadPool
import requests
import utils

GOOGLE_NEWS_RSS = "https://news.google.com/news/feeds?output=rss&q="
SPACE = "%20"
query = "benghazi"

query = query.replace(" ", "%20")
url = GOOGLE_NEWS_RSS+query
response = requests.get(url).text

# Get article links from the RSS
links = []
utils.find_links(links, response)
if len(links) > 1:
    links = links[2:]

# Get article titles from the RSS
titles = []
utils.find_titles(titles, response)
if len(titles) > 1:
    titles = titles[2:]

for i in range(len(links)):
    print(links[i], titles[i])

num_links = len(links)
articles = []
pool = ThreadPool(num_links)
for i in range(num_links):
    pool.add_task(
        utils.get_article_sentiment, links[i], articles)
pool.wait_completion()

sentiments = []

result = {}
result["articles"] = []
for i in range(num_links):
    info = {}
    info["title"] = titles[i]
    info["link"] = links[i]
    sentiments.append(articles[i]["sentiment"])
    info["sentiment"] = sentiments[i]
    info["snippet"] = articles[i]["snippet"]
    result["articles"].append(info)

average_sentiment = utils.average_sentiment(sentiments, num_links)  
result["sentiment"] = average_sentiment
print(result)
