from micropython import const
from ubluetooth import BLE
import ubluetooth
import ubinascii
import network
import struct


_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)

# Advertising payloads are repeated packets of the following form:
#   1 byte data length (N + 1)
#   1 byte type (see constants below)
#   N bytes type-specific data

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)

_CCT_DATA_TAG = "cct-dyw"


def decode_field(payload, adv_type):
    i = 0
    result = []
    while i + 1 < len(payload):
        if payload[i + 1] == adv_type:
            result.append(payload[i + 2:i + payload[i] + 1])
        i += 1 + payload[i]
    return result

def decode_name(payload):
    n = decode_field(payload, _ADV_TYPE_NAME)
    return str(n[0], "utf-8") if n else ""

def adv_encode(adv_type, value):
    return bytes((len(value) + 1, adv_type,)) + value

def adv_encode_name(name):
    return adv_encode(const(0x09), name.encode())

def _handle_coro(search_event, threshold, callback):
    while True:
        (event, data) = (yield)
        if event == search_event:
            print("New BT device scanned...")
            addr_type, addr, adv_type, rssi, adv_data = data
            address = str(ubinascii.hexlify(addr, ":"), "utf-8")
            data_tag = decode_name(adv_data)
            print("Signal strength: {}".format(rssi))
            if rssi > threshold and callback is not None and data_tag == _CCT_DATA_TAG:
                print("CCT Bluetooth device scanned...")
                callback(address)


class Proximity:

    """
    Detects device proximity using Bluetooth LE

    Example:

    .. code-block::

        from cct.proximity import Proximity
        # scanning example, see example.py for advertising
        p = Proximity()
        # activate bluetooth
        p.activate()
        # get bt mac address
        mac = p.bluetooth_mac_address
        # set threshold
        p.threshold = -100
        # set your callback function (see example.py)
        p.callback = your_predefined_callback
        p.start_scanning()
        # when you're done
        p.stop_scanning()
        p.deactivate()
    """

    def __init__(self, threshold=None, callback=None):
        """
        Initializes the proximity detecter
        """
        self._threshold = -100
        self.interval = 10
        self._callback = None
        self.bt = BLE()

    def _activate_bluetooth(self):
        # have to first activate wlan before bt due to bug:
        # https://github.com/micropython/micropython/issues/6423
        if not self.bt.active():
            print("Activating bluetooth...")
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            self.bt.active(True)

    def activate(self):
        self._activate_bluetooth()

    @property
    def threshold(self):
        """
        `number`: Threshold for proximity detection strength (default: -50)

        Adjust this threshold to set detect closer (higher) and farther (lower)
        """
        return self._threshold

    @threshold.setter
    def threshold(self, threshold):
        self._threshold = threshold

    @property
    def interval(self):
        """
        `number`: Scan interval in seconds (default: 10s)

        Adjust this interval between scans
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        self._interval = interval

    @property
    def callback(self):
        """
        callback ((event, data) -> None): Function passed to retrieve proximity event and data
        """
        return self._callback

    @callback.setter
    def callback(self, callback):
        self._callback = callback
        self._coroutine = _handle_coro(_IRQ_SCAN_RESULT, self._threshold, self._callback)
        self._coroutine.__next__()

    def _handle_irq(self, event, data):
        self._coroutine.send((event, data))

    def is_active(self):
        """
        Proximity bluetooth active status
        Returns:
            bool: is active?
        """
        return self.bt.active()

    def start_scanning(self):
        """
        Start proximity detection (start observing *other* bluetooth devices)
        """
        if not self.is_active():
            print("Bluetooth must be active before scanning")
            return False
        if self._coroutine is None:
            print("Alert: callback is not set, please set callback before starting to scan")
        else:
            self.bt.irq(self._handle_irq)
            self.bt.gap_scan(0, self.interval * 1000000, 100000)

    def stop_scanning(self):
        """
        Stop proximity detection (stop observing *other* bluetooth devices)
        """
        self.bt.gap_scan(None)

    def start_advertising(self):
        """
        Start advertising device signal (start signaling *to* other bluetooth devices)
        """
        self.bt.gap_advertise(100000, adv_data=adv_encode_name(_CCT_DATA_TAG), connectable=False)

    def stop_advertising(self):
        """
        Stop advertising device signal (stop signaling *to* other bluetooth devices)
        """
        self.bt.gap_advertise(None)

    @property
    def bluetooth_mac_address(self):
        """
        `str`: MAC address hex string

        Property for the MAC address ID for bluetooth device
        """
        u = ubinascii.hexlify(self.bt.config("mac")[1], ":")
        return str(u, "utf-8")

    def deactivate(self):
        self.bt.active(False)
