"""
Module: 'flashbdev' on micropython-esp32-1.13-274
"""
# MCU: {'ver': '1.13-274', 'port': 'esp32', 'arch': 'xtensawin', 'sysname': 'esp32', 'release': '1.13.0', 'name': 'micropython', 'mpy': 10757, 'version': '1.13.0', 'machine': 'ESP32 module with ESP32', 'build': '274', 'nodename': 'esp32', 'platform': 'esp32', 'family': 'micropython'}
# Stubber: 1.3.9

class Partition:
    ''
    BOOT = 0
    RUNNING = 1
    TYPE_APP = 0
    TYPE_DATA = 1
    def find():
        pass

    def get_next_update():
        pass

    def info():
        pass

    def ioctl():
        pass

    def mark_app_valid_cancel_rollback():
        pass

    def readblocks():
        pass

    def set_boot():
        pass

    def writeblocks():
        pass

bdev = None
