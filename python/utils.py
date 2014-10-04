import idol_sentiment as isent
from multiprocessing import Pool

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


TEST_ARTICLE = "My iPhone 6 Plus arrived in the mail last night, "
    "so I'm currently within the first few minutes of playing around "
    "with it. This was the first iPhone that I ever ordered online — "
    "my previous ones I bought in the store — and so it was the first "
    "time I've activated one myself. That turned out to be a breeze, "
    "so that was cool. Restoring my contacts, photos, and apps via "
    "iCloud also worked very nicely. Anyway, the iPhone has never been "
    "particularly good at capturing images in low light. But it's "
    "instantly clear that the new iPhone represents a major advance "
    "on this front."


def find_links(links, response):
    l = response.find(LINK)
    if l == NOT_FOUND:
        return
    else:
        e = response.find(END_LINK)
        full = response[l+LINK_LENGTH:e]
        u = full.find(URL)
        links.append(full[u+URL_LENGTH:])
        return find_links(links, response[e+END_LINK_LENGTH:])


def find_titles(titles, response):
    l = response.find(TITLE)
    if l == NOT_FOUND:
        return
    else:
        e = response.find(END_TITLE)
        full = response[l+TITLE_LENGTH:e]
        u = full.find(URL)
        titles.append(full[u+URL_LENGTH:])
        return find_titles(titles, response[e+END_TITLE_LENGTH:])


def get_article_sentiment(url):
    # TODO(john): add function to get article body
    article_body = TEST_ARTICLE
    lines = article_body.split("\n").strip()
    sentences = []
    for line in lines:
        if len(line) != 0:
            line_sentences = line.split(".")
            sentences = sentences + line_sentences
    sentences = extract_n_sentences(sentences, NUM_SENTENCES)

    pool = Pool(processes=NUM_SENTENCES)
    sentiments = pool.map(isent.find_sentence_sentiment, sentences)

    num_sentences = len(sentences)
    article_sentiment = average_sentiment(sentiments, num_sentences)
    if num_sentences == 0:
        return "", 0
    return sentences[0], article_sentiment


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
