try:
    import urequests as requests
except:
    import requests

try:
    import ujson as json
except:
    import json

from covidconnection.google.loadkey import LoadKey
from covidconnection.google.auth import ServiceAccount
from covidconnection.google import auth

class Firebase:

    """
    Reads, writes, modifies, and deletes objects to a Firebase database

    Attributes
    ----------

    database: string
        Firebase database name
    email: string
        Email for authenticated service account


    Methods
    -------

    get(key)
        Fetch a value from the database by key
    put(key, value)
        Write a value to the database by key
    delete(key):
        Delete a value from the database by key
    patch(key, value)
        Modify a value in the database by key
    post(key, value):
        Add a value to a list of values under key
    append_to_list(key, value)
        Alias for `post`
    get_list(key)
        Fetch a list from the database by key
        
    """
    def __init__(self, database, email, keyfile):
        """
        Initializes the Firebase database

        Parameters
        ----------
        database : str
            String name of the Firebase database
        email : str
            Email for service account used to authenticate
        keyfile : str
            Full filename to service account keyfile (e.g. `key.json`)
            A relative or full path to filename can be used
        Returns
            Instance of `Firebase` database
        -------
            
        """
        print("Authenticating to Firebase database...")
        loaded_key = LoadKey(keyfile)
        sa = ServiceAccount()
        sa.scope([auth.SCOPE_USERINFO_EMAIL, auth.SCOPE_FIREBASE_DATABASE])
        sa.private_rsa_key(loaded_key.key)
        sa.email(email)
        self._token = sa.token()
        self.email = email
        self.database = database

    def get(self, key):
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self.database, key, self._token)
        resp = requests.get(url)
        return resp.json()

    def delete(self, key):
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self.database, key, self._token)
        resp = requests.delete(url)
        return resp.json()

    def put(self, key, value):
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self.database, key, self._token)
        data = json.dumps(value)
        resp = requests.put(url, data=data)
        return resp.json()

    def patch(self, key, value):
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self.database, key, self._token)
        data = json.dumps(value)
        resp = requests.patch(url, data=data)
        return resp.json()

    def post(self, key, value):
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self.database, key, self._token)
        data = json.dumps(value)
        resp = requests.post(url, data=data)
        return resp.json()

    def get_list(self, key):
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self.database, key, self._token)
        resp = requests.get(url)
        d = resp.json()
        try:
            return list(d.values())
        # not a list
        except AttributeError:
            return None

    def append_to_list(self, key, value):
        return self.post(key, value)
