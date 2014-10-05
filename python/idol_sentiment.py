from idol_api import *
import codecs

def find_sentence_sentiment(sentence):
    # sentence = sentence.replace(" ", "%20")
    # Ensure the sentence is ascii
    sentence = ''.join([i if ord(i) < 128 else ' ' for i in sentence])
    args = {'text':sentence}
    response = APIRequest(APIEndpoints.GET_SENTIMENT, args).response()
    try:
        return (response["aggregate"]["score"]+1)/2.0
    except KeyError:
        return 0.5