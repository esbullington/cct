try:
    import ujson as json
except:
    import json

try:
    import urequests as requests
except:
    import requests

import covidconnection.google.ntp
from covidconnection.google.loadkey import LoadKey
from covidconnection.google.auth import ServiceAccount


class Spreadsheet:

    def __init__(self, token):
        self._id = ''
        self._range = ''
        self._url_params = 'insertDataOption=INSERT_ROWS&valueInputOption=USER_ENTERED'
        self._url_template = 'https://sheets.covidconnection.googleapis.com/v4/spreadsheets/%s/values/%s:append?%s'
        sa = ServiceAccount()
        sa.scope([auth.SCOPE_SPREADSHEETS])
        sa.private_rsa_key(keyfile)
        sa.email(email)
        self._token = sa.token()

    def set_id(self, id):
        self._id = id

    def set_range(self, range):
        self._range = range

    def append_values(self, values):
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
