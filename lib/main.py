import utime as time
from machine import Pin
import settings

Pin(2,Pin.OUT).value(0)
time.sleep(1.8)
if not Pin(0, Pin.IN, Pin.PULL_UP).value():  # D3 pulled to gnd (flash button pressed)??
    print("Abort")
    import sys
    sys.exit()  # if so,  abort
Pin(2,Pin.OUT).value(1)

import wifi
import sntp

gc.collect()
print("Mem: ", gc.mem_free(), "\nProject: ", settings.project)
exec("import " + settings.project)
gc.collect()
print("Mem: ", gc.mem_free())

#exec(open("./filename").read())
# https://stackoverflow.com/questions/436198/what-is-an-alternative-to-execfile-in-python-3

import Oled
