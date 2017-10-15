
import gc, micropython
from Oled import oled
import settings
settings.BlynkGpioAuto=True
from pblynk import Blynk

b=Blynk()
def cnct_cb():
    print ("Connected: ")
b.on_connect(cnct_cb)

b.gpio_auto()

def Tfunc(st):
    print(st, gc.mem_free())
    if oled:
        oled.invert(st & 1)
    return st+1
    
b.Ticker(Tfunc,200,5)

print( "Mem: ", gc.mem_free())
b.run()



# Automatically sets any GPIO writes from APP as OUTPUT,  and all GPIO reads (poll) from APP 

######################################################################################


# at APP:
# 3 buttons writing to GPIOs 21, 20, 16 (leds on rpi)
# 3 LEDs polling gpios 6, 26  19 (rpi buttons) and 14 (rpi pir)


