
# manually configured GPIOs


from Oled import oled
from pblynk import Blynk
b=Blynk()
from machine import Pin
from micropython import schedule



######################################################################################

#  Button1 poll mode
# Buttons or other inputs by manual coding. Direct GPIO (not Vpin) settings at app.
# Flexible. can make Button, InputDevice etc pulldown etc as desired.
# Slower latency

# generic gpio read by POLL from app

def gpioRead_h(pin, gpioObj):  
    v = gpioObj()
    return (1 if v else 0)

# set up any buttons (or whatever) and connect to gpioRead_h  - say D3 gpio 0 flash button
button1 = Pin(0, Pin.IN, Pin.PULL_UP)    
b.add_digital_hw_pin(0, gpioRead_h, None, button1)  # note the  button object is payload as "state"

######################################################################################

# pin.irq() allows only a callback functionname, with one automatic argument, the Pin object.
# partial() function from functools library allows us to send more arguments from .irq(), 
# namely the gpio pin number that we need for the blynk virtual write.
def partial(func, *args):
    # hacked from https://github.com/micropython/micropython-lib/blob/master/functools/functools.py
    def _partial(*more_args):
        return func(*(args + more_args))
    return _partial

def i2_cb(data):  # this generic fn set to send to VPin number corresponding to GPIO number
    #    data[0] = pinnumber, data[1] = pin.value(),
    b.virtual_write(data[0], data[1]*100)

def i_cb(pinnumber, pin): # pin (obj) was auto from .irq().  pinnumber added due to partial()
    # we are in interrupt. Reschedule real processing to later.
    schedule(i2_cb, [pinnumber, pin.value()]) # read value asap. Toss pin obj, just use pin gpio#
        
# Button D5 - push mode from 8266 gpio 14 - send to APP on VP14  
buttonD5 = Pin(14, Pin.IN, Pin.PULL_UP)
buttonD5.irq(partial(i_cb, 14), Pin.IRQ_FALLING|Pin.IRQ_RISING) 



######################################################################################

# 3 LEDs + inbuilt Led on D4:
def gpioWrite_h(val, pin, gpioObj): # generic gpio write   (GPIO settings at app)
    gpioObj.value(val)

# set up the RPi LEDs or other outputs and connect to generic gpioOut
ledR = Pin(12, Pin.OUT) 
ledG = Pin(13, Pin.OUT)

ledD4 = Pin(2, Pin.OUT)
b.add_digital_hw_pin(12, None, gpioWrite_h, ledR)
b.add_digital_hw_pin(13, None, gpioWrite_h, ledG)

b.add_digital_hw_pin(2, None, gpioWrite_h, ledD4)


#------------------------------

def cnct_cb():
    print ("Connected: ")
b.on_connect(cnct_cb)




######################################################################################

b.run()

######################################################################################

# at APP:
# 3 buttons writing to GPIOs 
# 3 led widgets listening to gpios 
# one value display widget polling gpio 
