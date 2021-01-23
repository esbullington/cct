import time

import network


# the class starts a WiFi access point
class AccessPoint:
    """
    Initialize a new WiFi access point

    Attributes
    ----------
    access_point_ssid : str
        SSID string for access point
    access_point_password : str
        Password for access point

    Methods
    -------
    start()
        Start the access point
    ip()
        returns an IP address of the access point

    Notes
    -----
    Make sure that the password is not too short. Otherwise, an
    OSError may occur while staring the access point.

    """

    def __init__(self, access_point_ssid, access_point_password):
        self.access_point_ssid = access_point_ssid
        self.access_point_password = access_point_password
        self.access_point = None

    def start(self):
        self.access_point = network.WLAN(network.AP_IF)
        self.access_point.active(True)
        self.access_point.config(essid=self.access_point_ssid,
                                 password=self.access_point_password,
                                 authmode=network.AUTH_WPA_WPA2_PSK)

    def ip(self):
        if self.access_point is None:
            raise Exception('Access point has not started!')
        return self.access_point.ifconfig()[0]


class Connection:
    """
    Maintains a connection to a WiFi network

    Parameters
    ----------

    ssid : str
        SSID for connection
    password : str
        Password for connection
    nic : str
        Connection NIC

    Methods
    -------

    connect()
        Connect to network
    is_connected()
        Check if connected 
    reconnect_if_necessary()
        Reconnect if necessary
    disconnect()
        Disconnect
    reconnect()
        Reconnect

    """
    # initialize a connection to a WiFi network
    def __init__(self, ssid, password):

        # check if ssid and password are specified
        if not ssid or not password:
            raise Exception('ssid/password are not set')

        self.ssid = ssid
        self.password = password
        self.nic = network.WLAN(network.STA_IF)

    # connect to the specified wi-fi network
    def connect(self):
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

    # check if the connection is active
    def is_connected(self):
        return self.nic is not None and self.nic.active() and self.nic.isconnected()

    # tries reconnecting if the connection is lost
    def reconnect_if_necessary(self):
        while not self.is_connected():
            self.connect()

    # disconnect from the network
    def disconnect(self):
        print('disconnecting ...')
        self.nic.disconnect()
        self.nic.active(False)

    # disconnect from the network and connect again
    def reconnect(self):
        self.disconnect()
        self.connect()
