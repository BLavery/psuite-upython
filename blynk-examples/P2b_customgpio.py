
# manually configured GPIOs


from Oled import oled
from pblynk import Blynk
b=Blynk()
from machine import Pin
from micropython import schedule
import utime as time



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

# interrupt button reads, debounced, sent to APP via vpin    


##########  UNTESTED ################

class blynkButton(object):
    def __init__(self, gpiopin, vpin):
        self.butn = Pin(gpiopin, Pin.IN, Pin.PULL_UP)
        self.butn.irq(self.i_cb, Pin.IRQ_FALLING|Pin.IRQ_RISING)
        self.ts=time.ticks_ms()
        self.vpin = vpin
        self.gpiopin = gpiopin
        
    def i_cb(self, pinObj):
        ts1 = time.ticks_ms()
        if time.ticks_diff(ts1, self.ts)< 100: # toss away keybounce spikes
            return
        self.ts = ts1
        try:
            schedule(self.i2_cb, None) # sched has small stack (4 !) and seems fragile anyway
        except:      
            pass

    def i2_cb(self,dummy): 
        time.sleep_ms(80)  # wait till after any bounce
        b.virtual_write(self.vpin, self.butn.value()*100) 

buttonD5 = blynkButton(14, 3)  # gpio 14 to send to vpin 3
buttonD1 = blynkButton(5, 4)

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
