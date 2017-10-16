
# P-Blynk   

# A MicroPython Blynk library for ESP8266
<img align="right" src="images/blynk.jpg">

## Intro

A single py file for blynk is too large to load in the ESP8266 available memory. It's the initial loading process that uses most memory, and once it's loaded and compiled to bytecode it is (just) workable in the memory available. I have tried to use the mpy-cross compiler to convert it to mpy bytecode, so far without success. I find certain syntax constructions that run in py code fail in mpy code. There may be a solution, but I haven't found it yet.

So the blynk library in pSuite is in py file(s) and is loaded in stages. You import pblynk.py and that chains to several files blynk_1.py, blynk_2.py etc automatically. The code is a crude stitch-together that does actually work. 

But be aware that the blynk library still leaves available RAM low (about 9-10 kB), and if your "project" code grows large, you should expect memory crashes. Use blynk for modest projects.

On your APP, use device type = **esp8266**. GPIO numbers are native chip GPIO references, not D0 D1 etc as labelled on some boards.

## Creating the blynk object

Your blynk token should be edited in your settings.py file.There are also 3 blynk options in settings:

-   BlynkBridge
-   BlynkExtras (sync, tweet, setproperty, lcd, email)
-   BlynkGpioAuto. 

These if True will add extra
functionality to Blynk, at the expense of precious RAM memory. These same settings
can be overridden in project file before you import blynk.

Normal startup:

	import pblynk 
	b = pblynk.Blynk() 

or in full:

	b = pblynk.Blynk(token, server, port, connect) 
	# defaults = settings.Token, "blynk-cloud.com", 8442, True 

-connection is TCP (no ssl option)

Adding options:

	import settings, machine
	settings.BlynkGpioAuto=True
	import pblynk 
	b = pblynk.Blynk()  
	b.gpio_auto(machine.Pin.PULL_UP)
    
At this point a blynk instance ("b") is created, but it has **not** tried to connect to the Blynk cloud.  
That is done with b.run(), which needs to be last line of script.
b.run() is a **blocking function**, and does NOT return to your script. 

 
## GPIO control with zero coding


	b.gpio_auto(Pull)  # where Pull = machine.Pin.PULL_UP or is omitted.
    
This causes all GPIOs that the phone APP is configured for will be 
automatically configured as inputs or outputs on the ESP8266. And GPIO
writes or reads (polls) issued by the APP will be handled at the ESP
without explicit coding. This function must be pre-optioned as above before importing blynk. 

The optional resistor pullup will apply to ALL the gpio autoconfigured as inputs.
 
Note that in many practical cases this will be too simplistic, and then custom coding is needed instead, as in the next section. 


## GPIO & Virtual Read & Write Callbacks


The callbacks are like this, and should be def'd before doing the add_xxx_pin():

	def digital_read_callback(pin, state):  
		digital_value = xxx       # access your hardware  
		return digital_value 
    
	def digital_write_callback(value, pin, state):  
		# access the necessary digital output and write the value  
		return

	def virtual_read_callback(pin, state):  
		virtual_value = 'Anything'       # access your hardware  
		return virtual_value    #  return may be None, or a single value, or a list of values  
		# if using return None, then arrange own virtual.write() back to APP,  
		# but the "correct" way is to "return" the value to APP 
            
	def virtual_write_callback(value, pin, state):  
		# NOTE: "value" is a LIST, so you need to unpack eg value[0] etc  
		# access the necessary virtual output and write the value
		return

Then you assign your gpio or virtual pins like this:

	b.add_digital_hw_pin(pin=pin_number, read=digital_read_callback, inital_state=None)  
	b.add_digital_hw_pin(pin=pin_number, write=digital_write_callback, inital_state=None)  
	b.add_virtual_pin(vpin_number, read=virtual_read_callback, inital_state=None)  
	b.add_virtual_pin(vpin_number, write=virtual_write_callback, inital_state=None)  
	# in this context, write means "APP writes to 8266 HW" and read is "APP polls HW expecting HW reply"

-  initial_state is an optional payload of one value.
-  That one initial-state value may possibly be one LIST of values if you want to really pass several.  
-  Gpio pins are actual GPIO hardware numbers.   
-  Virtual pins are 0 - 40.
-  There is no support for analog pins. Use a virtual pin as needed.

## User Task: the "Ticker":


It is possible to set up one periodic user task known as the Ticker. This is a function call from Blynk back to your project script. It is NOT a concurrent or threaded task.

  
Ticker is a repeating function 

-  Register and start (one only) simple "ticker" function callback.  
-  "divider" (default 40) divides into 200 to give ticker frequency. eg divider 100 gives 2 ticks / sec. Don't rely strictly on the timing. It may stretch slightly if blynk is busy.
-  Use "state" to carry any data between calls.
-  Callback suspends blynk until its return. Not concurrent. Ticker should exit promptly to not hold up blynk. (eg 3 mSec would be considered quite too long.)

Define your callback, then register your Ticker:

	def ticker_callback(state):  
		# do anything you like. Might be complex or long, but it should be still fast. 
		# Examine gpio pins? Do a virtual pin write? print to terminal or oled? ...
		return new_state   # or just return
	b.Ticker(ticker_callback, divider=40, initial_state = None)  
	b.Ticker(None) # disables !
    

## Software functions and widgets at python end:

	b.notify(message_text)

The following bridge group need to be optioned on in your settings:

	bridge = b.bridge_widget(my_vpin_number)   # all writes to this widget get bridged to other HW  
	bridge.set_auth_token(target_token)  # but first wait until "connected"! Use a on_connect() callback. 
	bridge.virtual_write(target_vpin, val)  # val = single param only, no lists  
	bridge.digital_write(target_gpiopin, val) 

*A "bridge" allows you to send writes across to another MCU also running blynk (RPi, 8266, etc). You devote one of your virtual pins as a channel via the server to the other device. And you need to know the separate token (on your blynk account) used by the other hardware.*

This next extras group also needs to be optioned on in your settings:
      
	b.lcd_print(vpinnumber, x, y, message) #  x=0-15   y=0-1  "advanced" mode at APP
	b.lcd_cls(vpinnumber)  
	b.email([to,] subject, body) # don't forget email widget on APP! 
	b.tweet(message_text)  # (same)
	b.virtual_write(vpin_number, value)
		# value = either single value (int/str) or list of values.  
		# For ad-hoc writing to a vpin (ie toward APP),  
		# without necessarily having done add_virtual_pin()
		# For this context, write means 8266 to APP
	b.set_property(vpin, property, value)  
		#  eg "color", "#ED9D00"    or "label"/"labels" "onLabel" etc  
    
The main non-returning loop of the blynk engine:

	b.run()    # Last line of python script 

And ...

	b.on_connect(connect_callback)  
	b.on_disconnect(disconnect_callback)  
	b.connect()  
	b.disconnect()

https://github.com/BLavery/psuite-upython/blob/master/pblynk.md  

This blynk is hacked down from PiBlynk: see https://github.com/BLavery/PiBlynk
