try:
    import ujson as json
except ImportError:
    import json

try:
    import urequests as requests
except ImportError:
    import requests

import covidconnection.google.ntp
from covidconnection.google.loadkey import LoadKey
from covidconnection.google.auth import ServiceAccount


class Spreadsheet:
    """
    Interacts programmatically with Google spreadsheet

    Example:

    .. code-block::

        from covidconnection.sheet import Spreadsheet
        spreadsheet = Spreadsheet('myserviceaccount@email`, `mykeyfile`)
        spreadsheet.set_id("fdsifwy89dafdhas") # ID can be found in sheet URL
        spreadsheet.set_range('A:A')
        spreadsheet.append_values([1, 2])
    """

    def __init__(self, email, keyfile):
        """
        Initializes the Firebase database


        Args:
            email (`str`): 
                Email for service account used to authenticate
            keyfile (`str`): 
                Full filename to service account keyfile (e.g. `key.json`)
                A relative or full path to filename can be used
        """
        self._id = ''
        self._range = ''
        self._url_params = 'insertDataOption=INSERT_ROWS&valueInputOption=USER_ENTERED'
        self._url_template = 'https://sheets.googleapis.com/v4/spreadsheets/%s/values/%s:append?%s'
        sa = ServiceAccount()
        sa.scope([auth.SCOPE_SPREADSHEETS])
        sa.private_rsa_key(keyfile)
        sa.email(email)
        self._token = sa.token()

    def set_id(self, id):
        """
        Sets current sheet by sheet ID

        Args:
            id (`str`): Sheet ID
        """
        self._id = id

    def set_range(self, range):
        """
        Sets current sheet range

        Args:
            range (`str`): Sheet range
        """
        self._range = range

    def append_values(self, values):
        """
        Appends values on current range

        Args:
            values (`[any]`): Values to append
        """
        print('spreadsheet: send: %s' % values)
        token = self._token
        url = self._url_template % (self._id, self._range, self._url_params)
        values.insert(0, ntp.time())
        data = {'values': [ values ]}
        headers = {}
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer %s' % token
        response = requests.post(url, json=data, headers=headers)
        if not response:
            print('spreadsheet: no response received')
        print('spreadsheet: response:')
        print(response.text)
