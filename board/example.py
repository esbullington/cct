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

wifi = Connection("ssid", "password")
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


def callback_function(addr):
    # here you can do whatever you need with the scanned MAC address
    print("CALLING BACK")

# proximity detection via bluetooth
from cct.proximity import Proximity
p = Proximity()
p.callback = callback_function
p.start_scanning()

# when you're done
p.stop_scanning()
p.deactivate()

# to advertise
p.start_advertising()
# to stop advertising
p.stop_advertising()
