from blynk_0 import *


def notify(self, msg):
    if self.state == AUTHENTICATED:
        self._send(self._format_msg(MSG_NOTIFY, msg))

def virtual_write(self, pin, val):
    if self.state == AUTHENTICATED:
        if type(val) == type([]):  
            val = '\0'.join(map(str, val)) 
        self._send(self._format_msg(MSG_HW, 'vw', pin, val))

def Ticker(self, func, divider = None, initial_state = None):
    if divider:
        self._tick_scale = divider
    self._on_tick = func
    self._tick_state = initial_state

def add_virtual_pin(self, pin, read=None, write=None, initial_state=None):
    if isinstance(pin, int) and pin in range(0, MAX_VIRTUAL_PINS):
        self._vr_pins[pin] = self.VrPin(read=read, write=write, blynk_ref=self, initial_state=initial_state)
    else:
        raise ValueError('pin only 0 to ' , (MAX_VIRTUAL_PINS - 1))

def add_digital_hw_pin(self, pin, read=None, write=None, inital_state=None):
    if isinstance(pin, int):
        self._digital_hw_pins[pin] = self.HwPin(read=read, write=write, blynk_ref=self, initial_state=inital_state)
    else:
        raise ValueError("pin value INTEGER!")
        
def on_connect(self, func):
    self._on_connect = func
    
def on_disconnect(self, func):
    self._on_disconnect = func

def connect(self):
    self._do_connect = True

def disconnect(self):
    self._do_connect = False


