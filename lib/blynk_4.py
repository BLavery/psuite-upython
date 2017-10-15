from blynk_0 import *
from machine import Pin

def gpio_auto(self, Pull = None):  # Pull must be None or machine.Pin.PULL_UP (ie 1)
    
    def gpioRead_h(pin, gpioObj):  
        v = gpioObj.value()
        return (1 if v else 0)

    def gpioWrite_h(val, pin, gpioObj): 
        gpioObj.value(val)

    def setup_cb(params):
        # do gpio setup 
        pairs = zip(params[0::2], params[1::2])
        for (pin, mode) in pairs:
            pin = int(pin)
            print(pin,mode)
            if mode == "out":
                led = Pin(pin, Pin.OUT)
                self.add_digital_hw_pin(pin, None, gpioWrite_h, led)
            if mode == "in":
                button = Pin(pin, Pin.IN, pull=Pull) # global pullup or not
                self.add_digital_hw_pin(pin, gpioRead_h, None, button)  
                # note the button / led objects are payload as "state"
                      
    self._on_setup=setup_cb

