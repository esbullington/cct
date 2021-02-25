# Append base path
# add project base directory to python path
# so we can access both cct and test dir
import usys
usys.path.append('.')
# show micropython path
print("Path: ")
print(usys.path)

from cct.google.ufirebase import Firebase
from tests.test_tools import assert_with_msg
import gc
import time
import os

gc.enable()

database = os.getenv("FIREBASE_DATABASE")
service_account = os.getenv("FIREBASE_SA")
keyfile_location = os.getenv("FIREBASE_KEYFILE")
fb = Firebase(database, service_account, keyfile_location)

fb.put("test_entry", "wwwzzzyyy")

v = fb.get("test_entry")

assert_with_msg(v == "wwwzzzyyy", "Firebase get failed")

fb.delete("test_entry")
not_found = fb.get("test_entry")

assert_with_msg(not_found is None, "Firebase delete failed")

fb.delete("test_list")

fb.append_to_list("test_list", "a")
fb.append_to_list("test_list", "b")

xs = fb.get_list("test_list")
xs.sort()

assert_with_msg(xs[1] == "b")

fb.delete("test_list")

print("ufirebase tests finished successfully")
