
from micropython import const
from ubluetooth import BLE
import ubluetooth

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

def handle_coro(search_event, threshold, callback):
    while True:
        (event, data) = (yield)
        if event == search_event:
            print("Scan result received")
            print(event)
            print(data)
            addr_type, addr, adv_type, rssi, adv_data = data
            if rssi > threshold and callback is not None:
                callback(addr)
                print("Addr : {}".format(addr))
                print("Rssi : {}".format(rssi))


class Proximity:

    def __init__(self, threshold=None, callback=None):
        if threshold is None:
            self._threshold = -50
        else:
            self._threshold = threshold
        self._callback = callback
        self._corou = handle_coro(_IRQ_SCAN_RESULT, self._threshold, self._callback)
        self._corou.__next__()
        self.bt = BLE()

    def handle_irq(self, event, data):
        self._corou.send((event, data))

    def start(self):
        self.bt.active(True)
        self.bt.irq(self.handle_irq)
        self.bt.gap_scan()

    def stop(self):
        self.bt.gap_scan(None)
        self.bt.active(False)

    def get_own_bluetooth_address(self):
        return self.bt.config("mac")
