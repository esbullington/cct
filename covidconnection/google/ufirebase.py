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

    Example:

    .. code-block::

        from covidconnection.ufirebase import Firebase
        firebase = Firebase('mydbname', 'myserviceaccount@email`, `mykeyfile`)
        firebase.put('name', 'Joe Q Public')
        firebase.get('name') # returns 'Joe Q Public'
    """

    def __init__(self, database, email, keyfile):
        """
        Initializes the Firebase database


        Args:
            database (`str`): 
                String name of the Firebase database
            email (`str`): 
                Email for service account used to authenticate
            keyfile (`str`): 
                Full filename to service account keyfile (e.g. `key.json`)
                A relative or full path to filename can be used

        """
        print("Authenticating to Firebase database...")
        loaded_key = LoadKey(keyfile)
        sa = ServiceAccount()
        sa.scope([auth.SCOPE_USERINFO_EMAIL, auth.SCOPE_FIREBASE_DATABASE])
        sa.private_rsa_key(loaded_key.key)
        sa.email(email)
        self._token = sa.token()
        self.email = email
        """email (`str`): Email for authenticated service account."""
        self.database = database
        """database (`str`): Firebase database name."""

    def get(self, key):
        """
        Fetch a value from the database by key

        Args:
            key (`str`): Search key value
        Returns:
            `any`: Retrieved  key
        """
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self.database, key, self._token)
        resp = requests.get(url)
        return resp.json()

    def delete(self, key):
        """
        Delete a value from the database by key

        Args:
            key (`str`): Search key value
        """
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self.database, key, self._token)
        resp = requests.delete(url)
        return resp.json()

    def put(self, key, value):
        """
        Write a value to the database by key

        Args:
            key (`str`): Search key value
            value (`any`): Value to write to the database
        """
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self.database, key, self._token)
        data = json.dumps(value)
        resp = requests.put(url, data=data)
        return resp.json()

    def patch(self, key, value):
        """
        Modify a value in the database by key

        Args:
            key (`str`): Search key value
            value (`any`): Value to modify in the database
        """
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self.database, key, self._token)
        data = json.dumps(value)
        resp = requests.patch(url, data=data)
        return resp.json()

    def post(self, key, value):
        """
        Add a value to a list of values under key

        Args:
            key (`str`): Search key value
            value (`any`): Value to add to existing list
        """
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self.database, key, self._token)
        data = json.dumps(value)
        resp = requests.post(url, data=data)
        return resp.json()

    def append_to_list(self, key, value):
        """
        Alias for `post`

        Args:
            key (`str`): Search key value
            value (`any`): Value to add to existing list
        """
        return self.post(key, value)

    def get_list(self, key):
        """
        Fetch a list from the database by key

        Args:
            key (`str`): Search key value
        Returns:
            `[any]`: List retrived from database
        """
        url = "https://{}.firebaseio.com/{}.json?access_token={}".format(self.database, key, self._token)
        resp = requests.get(url)
        d = resp.json()
        try:
            return list(d.values())
        # not a list
        except AttributeError:
            return None
