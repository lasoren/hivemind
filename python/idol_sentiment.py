import codecs
import urllib.request
import json
import string

BASE = "https://api.idolondemand.com/1/api/sync/detectsentiment/v1?apikey="

IDOL_API_KEY = "ef2c248e-a32d-47d2-836f-692976c55ead"

TEXT = "&text="

SPACE = "%20"

def find_sentence_sentiment(sentence):
    sentence = sentence.replace(" ", "%20")
    # Ensure the sentence is ascii
    sentence = ''.join([i if ord(i) < 128 else ' ' for i in sentence])
    url = BASE+IDOL_API_KEY+TEXT+sentence
    print(url)
    response =  json.loads(
        str(urllib.request.urlopen(url).read()))
    print(response)
    return response["aggregate"]["score"]