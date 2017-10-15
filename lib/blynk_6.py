from blynk_0 import *


class BRIDGE: 
    def __init__(self, blynk, pin):
        self._blynk = blynk
        self._pin = pin
        
    def set_auth_token(self, target_token):   # but wait until "connected" !
        self._blynk._bridge_write( [str(self._pin),  "i", target_token])
        
    def digital_write(self, target_gpiopin, val):
        self._blynk._bridge_write( [str(self._pin),  "dw", target_gpiopin, val])
        
    def virtual_write(self, target_vpin, val):
        self._blynk._bridge_write( [str(self._pin),  "vw", target_vpin, val])

def bridge_widget(self, pin):
    brw = self.BRIDGE(self, pin)
    self.add_virtual_pin(pin)
    return brw

def _bridge_write(self, val):
    if self.state == AUTHENTICATED:
        if type(val) == type([]):             
            val = '\0'.join(map(str, val))  
        self._send(self._format_msg(MSG_BRIDGE,  val))

