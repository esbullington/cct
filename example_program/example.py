from google.ufirebase import Firebase
from config import Config
from wifi import AccessPoint
from wifi import Connection
import gc

# enable garbage collection
gc.enable()
print('garbage collection threshold: ' + str(gc.threshold()))

# load the config, make sure you have appropriate settings
# for your Firebase database and wifi network
config = Config("main.conf")

# initialize Firebase database
email = config.get("google_service_account_email")
db = config.get("firebase_database")
keyfile = config.get("google_keyfile")

# authenticate
fb = Firebase(db, email, keyfile)

def write_key_value_to_database(key, value)
    fb.put(key, value)

def wifi():
    # try to connect to WiFi if the configuration mode is disabled
    wifi = Connection(config.get('ssid'), config.get('password'))
    wifi.connect()
    return wifi
