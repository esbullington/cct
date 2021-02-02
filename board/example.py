# detailed comments for teaching

# these are esp32 system libraries we'll need

# this is a technical requirement for esp32
import gc

# we'll need the wifi connection module
from cct.wifi import Connection

# we'll need the Firebase module to connect to database
from cct.google.ufirebase import Firebase

# enable garbage collection
gc.enable()

wifi = Connection(("ssid", "password")
wifi.connect()

# variables needed to authenticate/initialize Firebase database
email = "google_service_account_id@someaccount.iam.gserviceaccount.com"
db = "firebase_database_name4243243-db"
keyfile = "key.json"

# authenticate/initialize database
fb = Firebase(db, email, keyfile)

# at this point, you can read and write to database
# writing
fb.put("yourkey", "somevalue")

# reading
v = fb.get("yourkey") # now v is equal to "somevalue"
