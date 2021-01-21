from covidconnection.google.ufirebase import Firebase
from covidconnection.wifi import AccessPoint
from covidconnection.wifi import Connection
from covidconnection.config import Config
import gc
import uos

# enable garbage collection
gc.enable()
print('garbage collection threshold: ' + str(gc.threshold()))

# load the config, make sure you have appropriate settings
# for your Firebase database and wifi network
config = Config("main.conf")

## if we're running on esp32 (not desktop), then start up the wifi
if usys.platform != "esp32":
    wifi = Connection(config.get('ssid'), config.get('password'))
    wifi.connect()

# initialize Firebase database
email = config.get("google_service_account_email")
db = config.get("firebase_database")
keyfile = config.get("google_keyfile")

# authenticate
fb = Firebase(db, email, keyfile)
