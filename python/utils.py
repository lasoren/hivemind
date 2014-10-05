import idol_sentiment as isent
from article import *

LINK = "<link>"
LINK_LENGTH = len(LINK)
END_LINK = "</link>"
END_LINK_LENGTH = len(END_LINK)
TITLE = "<title>"
TITLE_LENGTH = len(TITLE)
END_TITLE = "</title>"
END_TITLE_LENGTH = len(END_TITLE)
NOT_FOUND = -1

URL = "url="
URL_LENGTH = len(URL)

NUM_SENTENCES = 5


TEST_ARTICLE = ("My iPhone 6 Plus arrived in the mail last night, "
    "so I'm currently within the first few minutes of playing around "
    "with it. This was the first iPhone that I ever ordered online "
    "my previous ones I bought in the store and so it was the first "
    "time I've activated one myself. That turned out to be a breeze, "
    "so that was cool. Restoring my contacts, photos, and apps via "
    "iCloud also worked very nicely. Anyway, the iPhone has never been "
    "particularly good at capturing images in low light. But it's "
    "instantly clear that the new iPhone represents a major advance on "
    "this front.")


def find_links(links, response):
    l = response.find(LINK)
    if l == NOT_FOUND:
        return
    else:
        e = response.find(END_LINK)
        full = response[l+LINK_LENGTH:e]
        u = full.find(URL)
        links.append(full[u+URL_LENGTH:])
        return find_links(links, response[e+END_LINK_LENGTH-1:])


def find_titles(titles, response):
    l = response.find(TITLE)
    if l == NOT_FOUND:
        return
    else:
        e = response.find(END_TITLE)
        full = response[l+TITLE_LENGTH:e]
        titles.append(full)
        return find_titles(titles, response[e+END_TITLE_LENGTH-1:])


def get_article_sentiment(url, title, articles):
    article = Article(url)
    article_body = article.text
    lines = article_body.split("\n")
    article_sentiment = isent.find_sentence_sentiment(article_body)

    result = {}
    result["snippet"] = article.summary
    result["sentiment"] = article_sentiment
    result["title"] = title
    articles[url] = result


def get_article_entities(url, entities):
    article = Article(url)
    entities.append(article.all_entities)


def average_sentiment(sentiments, num_links):
    return sum(sentiments) / float(num_links)


def extract_n_sentences(sentences, n):
    important_sentences = []
    num_sentences = len(sentences)
    x = 1
    for i in range(n-1):
        if x < num_sentences:
            important_sentences.append(sentences[x])
            x = x*2
    important_sentences.append(sentences[num_sentences-1])
    return important_sentences
