from blynk_0 import *
import gc, settings

    
class Blynk:
    def __init__(self, token=None, server='blynk-cloud.com', port=8442, connect=True):
        self._vr_pins = {}
        self._do_connect = False
        self._on_connect = None
        self._on_disconnect = None
        self._on_setup = None
        self._on_tick = None
        self._tick_scale = 40
        self._tick_count = 0
        self._tick_state = None
        self._token = token if token else settings.Token 
        if isinstance(self._token, str):
            self._token = str.encode(self._token)
        self._server = server
        self._port = port
        self._do_connect = connect
        self._digital_hw_pins = {}
        self.state = DISCONNECTED
        self._failed_pings = 0
        


    class VrPin:
        def __init__(self, read=None, write=None, blynk_ref=None, initial_state=None):
            self.read = read
            self.write = write
            self.state = initial_state if initial_state is not None else {}
            self.blynk_ref = blynk_ref


    class HwPin:
        def __init__(self, read=None, write=None, blynk_ref=None, initial_state=None):
            self.read = read
            self.write = write
            self.state = initial_state if initial_state is not None else {}
            self.blynk_ref = blynk_ref

       

# separately import the bulk of class Blynk's member functions, 
# in layers (to avoid memory crash),
# and attach them all into class Blynk:

import blynk_1
import blynk_2 
import blynk_3
# 1-3 = blynk core.  4-6 = optional
blynk_4=""
if settings.BlynkGpioAuto:
    import blynk_4  # adds 900 b
gc.collect()
blynk_5=""
if settings.BlynkExtras:
    import blynk_5  # adds 1250 b
gc.collect()
blynk_6=""
if settings.BlynkBridge:
    import blynk_6  # adds 1280 b
gc.collect()

for bl in (blynk_1, blynk_2, blynk_3, blynk_4, blynk_5, blynk_6):
  for a in dir(bl): 
    typ=str(getattr(bl,a))[0:5]
    if typ == ("<func" or typ == "<clas") and a != "Pin"  and a != "const": 
        exec("Blynk."+a+"=bl."+a)

gc.collect()
print("Mem: ", gc.mem_free())
