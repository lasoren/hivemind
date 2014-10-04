import urllib.request
import json

BASE = "https://api.idolondemand.com/1/api/sync/detectsentiment/v1?apikey="

IDOL_API_KEY = "ef2c248e-a32d-47d2-836f-692976c55ead"

SPACE = "%20"

def find_sentence_sentiment(sentence):
    sentence = sentence.replace(" ", "%20")
    url = BASE+IDOL_API_KEY+sentence
    response =  json.loads(
        str(urllib.request.urlopen(url).read()))
    return response["aggregate"]["score"]