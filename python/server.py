from flask import Flask
from flask import Response
from flask import request
import json
from thread_pool import ThreadPool
import requests
import utils
import json
from copy import deepcopy
from collections import defaultdict

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
    query2 = query.replace(" ", "%20")
    
    json_data = json.loads(requests.get("http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + query2).text)
    json_data['echo'] = query
    json_data['echo2'] = query2
    return Response(json.dumps(json_data), mimetype='application/json')

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
        num_titles = len(titles)
        if num_titles > 3:
            num_titles = 3
        if num_titles < num_links:
            links = links[:num_titles]
        if num_links > 3:
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
            print query, ':', articles[key]["sentiment"]
            sentiments.append(articles[key]["sentiment"])

        average_sentiment = utils.average_sentiment(
            sentiments,
            len(sentiments))
        print average_sentiment
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
        if start_url in app.single_url_entity_cache:
            return Response(
                json.dumps(app.single_url_entity_cache[start_url]),
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


        entity_dict = defaultdict(int)
        for entity_list in enumerate(entities):
            for entity in entity_list:
                entity_dict[entity] += 1
        entities_list = list(sorted(entity_dict.items(), key=lambda x: x[1]))
        if len(entities_list > 5):
            entities_list = entities_list[:5]

        fix_entities = False
        if not entities_list:
            fix_entities = True

        if num_entities > 0:
            entities_set = entities[0]
            if fix_entities:
                if len(entities[0]) > 3:
                    entities_list = [word.title() for word in list(entities[0])[:3]]
                else:
                    entities_list = [word.title() for word in entities[0]]
            result[0] = [word.title() for word in entities[0]]
            for i in range(1, num_entities):
                if fix_entities and len(entities_list) < 3:
                    if len(entities[i]) + len(entities_list) > 3:
                        entities_list.extend([word.title() for word in list(entities[i])[:3-len(entities_list)]])
                    else:
                        entities_list.extend([word.title() for word in entities[i]])
                result[i] = [word.title() for word in entities[i]]

        result["entities"] = entities_list
        app.entity_cache[query] = deepcopy(result)


        return Response(json.dumps(result), mimetype='application/json')



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
