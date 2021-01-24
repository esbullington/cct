import time
import network


# the class starts a WiFi access point
class AccessPoint:
    """
    Initialize a new WiFi access point

    Notes:

    Make sure that the password is not too short. Otherwise, an
    OSError may occur while staring the access point.

    """

    def __init__(self, access_point_ssid, access_point_password):
        self.access_point_ssid = access_point_ssid
        """SSID string for access point"""
        self.access_point_password = access_point_password
        """Password for access point"""
        self.access_point = None

    def start(self):
        """
        Start the access point
        """
        self.access_point = network.WLAN(network.AP_IF)
        self.access_point.active(True)
        self.access_point.config(essid=self.access_point_ssid,
                                 password=self.access_point_password,
                                 authmode=network.AUTH_WPA_WPA2_PSK)

    def ip(self):
        """
        returns an IP address of the access point
        """
        if self.access_point is None:
            raise Exception('Access point has not started!')
        return self.access_point.ifconfig()[0]


class Connection:
    """
    Initializes a connection to a WiFi network

    ..code-block::

        from cct.wifi import Connection
        wifi = Connection("ssid", "password")
        wifi.connect()
    """
    def __init__(self, ssid, password):

        # check if ssid and password are specified
        if not ssid or not password:
            raise Exception('ssid/password are not set')

        self.ssid = ssid
        """SSID for connection"""
        self.password = password
        """Password for connection"""
        self.nic = network.WLAN(network.STA_IF)
        """Connection NIC"""

    def connect(self):
        """
        Connect to the previously specified wi-fi network
        """
        print('connecting to network: %s' % self.ssid)
        self.nic.active(True)
        self.nic.connect(self.ssid, self.password)

        attempt = 0
        while attempt < 30 and not self.nic.isconnected():
            time.sleep(1)
            attempt = attempt + 1
            print('still connecting ...')

        if self.nic.isconnected():
            print('connected')
        else:
            print('could not connect to WiFi')

    def is_connected(self):
        """
        Check if the connection is active
        Returns:
            bool: `True` if connection active, otherwise `False`
        """
        return self.nic is not None and self.nic.active() and self.nic.isconnected()

    def reconnect_if_necessary(self):
        """
        Reconnect if necessary
        """
        while not self.is_connected():
            self.connect()

    def disconnect(self):
        """
        Disconnect
        """
        print('disconnecting ...')
        self.nic.disconnect()
        self.nic.active(False)

    def reconnect(self):
        """
        Reconnect
        """
        self.disconnect()
        self.connect()
