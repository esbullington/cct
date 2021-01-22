try:
    import urequests as requests
except ImportError:
    import requests

try:
    import ujson as json
except ImportError:
    import json

from covidconnection.google.loadkey import LoadKey
from covidconnection.google.auth import ServiceAccount
from covidconnection.google import auth

class Firebase:

    def __init__(self, database, email, keyfile):
        print("Authenticating to Firebase database...")
        loaded_key = LoadKey(keyfile)
        sa = ServiceAccount()
        sa.scope([auth.SCOPE_USERINFO_EMAIL, auth.SCOPE_FIREBASE_DATABASE])
        sa.private_rsa_key(loaded_key.key)
        sa.email(email)
        self._token = sa.token()
        self._db = database

    def get(self, key):
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self._db, key, self._token)
        resp = requests.get(url)
        return resp.json()

    def put(self, key, value):
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self._db, key, self._token)
        data = json.dumps(value)
        resp = requests.put(url, data=data)
        return resp.json()

    def patch(self, key, value):
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self._db, key, self._token)
        data = json.dumps(value)
        resp = requests.patch(url, data=data)
        return resp.json()

    def post(self, key, value):
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self._db, key, self._token)
        data = json.dumps(value)
        resp = requests.post(url, data=data)
        return resp.json()

    def get_list(self, key):
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self._db, key, self._token)
        resp = requests.get(url)
        d = resp.json()
        try:
            return list(d.values())
        # not a list
        except AttributeError:
            return None

    def append_to_list(self, key, value):
        return self.post(key, value)
