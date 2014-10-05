from flask import Flask
from flask import Response
from flask import request
import json
from thread_pool import ThreadPool
import requests
import utils
import json
from copy import deepcopy

GOOGLE_NEWS_RSS = "https://news.google.com/news/feeds?output=rss&q="
SPACE = "%20"
query = "iphone"

app = Flask(__name__)

@app.before_first_request
def initialize():
    app.pool = ThreadPool(5)
    app.cache = {}
    app.entity_cache = {}
    app.sentiment_cache = {}
    app.single_url_entity_cache = {}

@app.route('/api/images', methods=['POST'])
def images():
    query = request.form['query']
    query = query.replace(" ", "%20")
    
    return Response(requests.get("http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + query).text, mimetype='application/json')

@app.route('/api/articles', methods=['POST'])
def articles():
    error = None
    if request.method == 'POST':
        query = request.form['query'].lower()
        query = query.replace(" ", "%20")
        if query in app.cache:
            return Response(json.dumps(app.cache[query]), mimetype='application/json')
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
        index = 0
        for key in articles:
            info = {}
            info["id"] = index
            index += 1
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
        app.cache[query] = deepcopy(result)
        return Response(json.dumps(result), mimetype='application/json')


@app.route('/api/sentiment', methods=['POST'])
def sentiment():
    error = None
    if request.method == 'POST':
        query = request.form['query']
        query = query.replace(" ", "%20")
        if query in app.sentiment_cache:
            return Response(
                json.dumps(app.sentiment_cache[query]),
                mimetype='application/json')
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
        num_titles = 3
        if num_titles < num_links:
            links = links[:num_titles]
        num_titles = len(links)
        num_links = 3
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
        for key in articles:
            sentiments.append(articles[key]["sentiment"])

        average_sentiment = utils.average_sentiment(
            sentiments,
            len(sentiments))
        result["sentiment"] = average_sentiment
        result["query"] = request.form['query']
        app.sentiment_cache[query] = deepcopy(result)
        return Response(json.dumps(result), mimetype='application/json')


@app.route('/api/entity', methods=['POST'])
def entity():
    error = None
    if request.method == 'POST':
        url = str(request.form['url'])
        start_url = deepcopy(url)
        if url in app.single_url_entity_cache:
            return Response(
                json.dumps(app.sentiment_cache[start_url]),
                mimetype='application/json')
        entities = []
        utils.get_article_entities(url, entities, False)
        result = {}
        entities_list = [word for word in entities[0]]
        result["entities"] = entities_list
        app.single_url_entity_cache[start_url] = deepcopy(result)
        return Response(json.dumps(result), mimetype='application/json') 

@app.route('/api/entities', methods=['POST'])
def entities():
    error = None
    if request.method == 'POST':
        query = request.form['query'].lower()
        query = query.replace(" ", "%20")
        if query in app.entity_cache:
            return Response(json.dumps(app.entity_cache[query]), mimetype='application/json')
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

        result = {}
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
        result["entities"] = entities_list

        if num_entities > 0:
            entities_set = entities[0]
            result[0] = [word.title() for word in entities[0]]
            for i in range(1, num_entities):
                result[i] = [word.title() for word in entities[i]]
        app.entity_cache[query] = deepcopy(result)
        result["entities"] = []
        return Response(json.dumps(result), mimetype='application/json')



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
