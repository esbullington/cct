import uos
import usys
import gc

print("Paths: ")
print(usys.path)

from covidconnection.google.ufirebase import Firebase
from covidconnection.config import Config

# enable garbage collection
gc.enable()
print("Starting garbage collection at threshold: " + str(gc.threshold()))

# load the config, make sure you have appropriate settings
# for your Firebase database and wifi network
config = Config("main.conf")

## if we"re running on esp32 (not desktop), then start up the wifi
if usys.platform == "esp32":
    from covidconnection.wifi import AccessPoint
    from covidconnection.wifi import Connection
    wifi = Connection(config.get("ssid"), config.get("password"))
    wifi.connect()

# initialize Firebase database
email = config.get("google_service_account_email")
db = config.get("firebase_database")
keyfile = config.get("google_keyfile")

# authenticate
fb = Firebase(db, email, keyfile)
