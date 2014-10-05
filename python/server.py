from flask import Flask
from flask import Response
from flask import request
import json
from thread_pool import ThreadPool
import requests
import utils
import json

GOOGLE_NEWS_RSS = "https://news.google.com/news/feeds?output=rss&q="
SPACE = "%20"
query = "iphone"

app = Flask(__name__)

@app.before_first_request
def initialize():
    app.pool = ThreadPool(5)

@app.route('/api/articles', methods=['POST'])
def articles():
    error = None
    if request.method == 'POST':
        query = request.form['query']
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
        return Response(json.dumps(result), mimetype='application/json')

@app.route('/api/entities', methods=['POST'])
def entities():
    error = None
    if request.method == 'POST':
        query = request.form['query']
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

        num_links = len(links)
        entities = []
        pool = ThreadPool(num_links)
        for i in range(num_links):
            pool.add_task(
                utils.get_article_entities, links[i], entities)
        pool.wait_completion()

        num_entities = len(entities)
        if num_entities > 0:
            previous_set = entities[0]
            final_set = entities[0]
            index = 1
            while index < num_entities and len(final_set) > 5:
                final_set = previous_set.intersection(entities[index])
                if len(final_set) > 5:
                    previous_set = final_set
        entities_list = [word.title() for word in previous_set]

    	if num_entities > 0:
    	    entities_set = entities[0]
    	    for i in range(1, num_entities):
    		entities_set.union(entities[i])
    	    entities_list = [word.title() for word in entities_set]
    	    result = {}
            result["entities"] = entities_list
            return Response(json.dumps(result), mimetype='application/json')
    	result = {}
    	result["entities"] = []
        return Response(json.dumps(result), mimetype='application/json')
	


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
