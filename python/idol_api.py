import requests
import urllib
import json


class APIEndpoints(object):

    EXTRACT_ENTITIES = 'https://api.idolondemand.com/1/api/sync/extractentities/v1'
    GET_SENTIMENT = "https://api.idolondemand.com/1/api/sync/detectsentiment/v1"


class DefaultAPIConfig(object):

    API_KEY = 'ef2c248e-a32d-47d2-836f-692976c55ead'


class APIRequest(object):

    def _process_args(self, args):
        filtered_args = {}
        extra_args = ''
        for argk, argv in args.items():
            if isinstance(argv, list):
                for v in argv:
                    extra_args += argk + '=' + v + '&'
            else:
                filtered_args[argk] = argv
        args = urllib.urlencode(filtered_args) 
        if extra_args:
            args += '&' + extra_args[:-1]
        return args

    def __init__(self, url, args, config=DefaultAPIConfig):
        self.url = url
        if config.API_KEY:
            args['apikey'] = config.API_KEY
        self.args = self._process_args(args)

    def response(self):
        r = requests.get(self.url + '?' + self.args)
        return r.json()
