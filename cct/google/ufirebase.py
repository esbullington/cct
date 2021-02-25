try:
    import urequests as requests
except:
    import requests

try:
    import ujson as json
except:
    import json

from cct.google.loadkey import LoadKey
from cct.google.auth import ServiceAccount
from cct.google import auth

class Firebase:
    """
    Reads, writes, modifies, and deletes objects to a Firebase database

    Example:

    .. code-block::

        from cct.ufirebase import Firebase
        firebase = Firebase('mydbname', 'myserviceaccount@email`, `mykeyfile`)
        firebase.put('name', 'Joe Q Public')
        firebase.get('name') # returns 'Joe Q Public'
    """

    def __init__(self, database, email, keyfile=None, proxy=None):
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
        print("Creating Firebase connection...")
        if keyfile is not None:
            print("Authenticating to Firebase database...")
            loaded_key = LoadKey(keyfile)
            sa = ServiceAccount()
            sa.scope([auth.SCOPE_USERINFO_EMAIL, auth.SCOPE_FIREBASE_DATABASE])
            sa.private_rsa_key(loaded_key.key)
            sa.email(email)
            self._token = sa.token()
            print("Authentication successful")
        else:
            self._token = None
        self._email = email
        """email (`str`): Email for authenticated service account."""
        self._database = database
        """database (`str`): Firebase database name."""
        if proxy is None:
            self._firebase = "https://{}.firebaseio.com".format(self._database)
        else:
            self._firebase = "http://{}".format(proxy)

    def get(self, key):
        """
        Fetch a value from the database by key

        Args:
            key (`str`): Search key value
        Returns:
            `any`: Retrieved  key
        """
        if self._token is None:
            url = "{}/{}.json".format(self._firebase, key)
        else:
            url = "{}/{}.json?access_token={}".format(self._firebase, key, self._token)
        resp = requests.get(url)
        return resp.json()

    def delete(self, key):
        """
        Delete a value from the database by key

        Args:
            key (`str`): Search key value
        """
        if self._token is None:
            url = "{}/{}.json".format(self._firebase, key)
        else:
            url = "{}/{}.json?access_token={}".format(self._firebase, key, self._token)
        resp = requests.delete(url)
        return resp.json()

    def put(self, key, value):
        """
        Write a value to the database by key

        Args:
            key (`str`): Search key value
            value (`any`): Value to write to the database
        """
        if self._token is None:
            url = "{}/{}.json".format(self._firebase, key)
        else:
            url = "{}/{}.json?access_token={}".format(self._firebase, key, self._token)
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
        if self._token is None:
            url = "{}/{}.json".format(self._firebase, key)
        else:
            url = "{}/{}.json?access_token={}".format(self._firebase, key, self._token)
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
        if self._token is None:
            url = "{}/{}.json".format(self._firebase, key)
        else:
            url = "{}/{}.json?access_token={}".format(self._firebase, key, self._token)
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
        if self._token is None:
            url = "{}/{}.json".format(self._firebase, key)
        else:
            url = "{}/{}.json?access_token={}".format(self._firebase, key, self._token)
        resp = requests.get(url)
        d = resp.json()
        try:
            return list(d.values())
        # not a list
        except AttributeError:
            return None
