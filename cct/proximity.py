from micropython import const
from ubluetooth import BLE
import ubinascii
import network

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


def memoryview_addr_to_str(data):
    ubinascii.hexlify(bytes(data), ":")

def memoryview_data_to_str(data):
    ubinascii.hexlify(bytes(data))

def _handle_coro(search_event, threshold, callback):
    while True:
        (event, data) = (yield)
        if event == search_event:
            print("***********************")
            print("Scan result received...")
            addr_type, addr, adv_type, rssi, adv_data = data
            print("Addr : {}".format(bytes(addr)))
            print("Rssi : {}".format(rssi))
            print("Threshold : {}".format(threshold))
            print("Adv data : {}".format(bytes(adv_data)))
            if rssi > threshold and callback is not None:
                print("...and signal scanned is greater than threshold, calling callback function with detected MAC address.")
                callback(addr)


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
        self._threshold = -50
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
            self.bt.gap_scan()

    def stop_scanning(self):
        """
        Stop proximity detection (stop observing *other* bluetooth devices)
        """
        self.bt.gap_scan(None)

    def start_advertising(self):
        """
        Start advertising device signal (start signaling *to* other bluetooth devices)
        """
        self.bt.gap_advertise(1000, adv_data="cct-dyw", connectable=False)

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
        return ubinascii.hexlify(self.bt.config("mac")[1], ":")

    def deactivate(self):
        self.bt.active(False)
