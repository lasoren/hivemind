from flask import Flask
from flask import Response
from flask import request

from multiprocessing.pool import ThreadPool
import requests
import utils

GOOGLE_NEWS_RSS = "https://news.google.com/news/feeds?output=rss&q="
SPACE = "%20"
query = "iphone"

app = Flask(__name__)

@app.route('/api/articles', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        query = request.form['query']
        query = query.replace(" ", "%20")
        url = GOOGLE_NEWS_RSS+query
        response = requests.get(url).text

        # Get article links from the RSS
        links = []
        utils.find_links(links, response)
        links = links[2:]

        # Get article titles from the RSS
        titles = []
        utils.find_titles(titles, response)

        num_links = 5
        pool = ThreadPool(processes=num_links)
        articles = pool.map(utils.get_article_sentiment, links[:num_links])
        # for i in range(num_links):
        # utils.get_article_sentiment(links[0])

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
    return Response(json.dump(result), mimetype='application/json')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
