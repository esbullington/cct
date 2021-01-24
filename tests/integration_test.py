import uos
import usys
import gc

# Append base path
usys.path.append('.')
# show micropython path
print("Path: ")
print(usys.path)

from cct.google.ufirebase import Firebase
from cct.config import Config

# enable garbage collection
gc.enable()
print("Starting garbage collection at threshold: " + str(gc.threshold()))

# load the config, make sure you have appropriate settings
# for your Firebase database and wifi network
config = Config("./tests/main.conf")

## if we"re running on esp32 (not desktop), then start up the wifi
if usys.platform == "esp32":
    from cct.wifi import AccessPoint
    from cct.wifi import Connection
    wifi = Connection(config.get("ssid"), config.get("password"))
    wifi.connect()

# initialize Firebase database
email = config.get("google_service_account_email")
db = config.get("firebase_database")
keyfile = config.get("google_keyfile")

# authenticate
def test_firebase():
    fb = Firebase(db, email, keyfile)
    fb.put("rewjkl32", 100)
    result = fb.get("rewjkl32")
    assert result == 100, "firebase get result not equal"
    fb.delete("rewjkl32")

if __name__ == "__main__":
    test_firebase()
