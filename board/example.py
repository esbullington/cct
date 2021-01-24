# detailed comments for teaching

# these are esp32 system libraries we'll need
import uos
import usys
import gc

# we'll need the Firebase module to connect to database
from cct.google.ufirebase import Firebase

# we have a special module for configuration
from cct.config import Config

# enable garbage collection
gc.enable()
print("Starting garbage collection at threshold: " + str(gc.threshold()))

# load the config file, check it to be sure you have appropriate settings
# for your Firebase database and wifi network
config = Config("main.conf")

## if we"re running on esp32 (not desktop), then start up the wifi
if usys.platform == "esp32":
    from cct.wifi import Connection
    wifi = Connection(config.get("ssid"), config.get("password"))
    wifi.connect()

# initialize Firebase database
email = config.get("google_service_account_email")
db = config.get("firebase_database")
keyfile = config.get("google_keyfile")

# authenticate
fb = Firebase(db, email, keyfile)

# at this point, you can read and write to database
