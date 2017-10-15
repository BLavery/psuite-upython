from micropython import const

##### For WIFI:
known_networks= [
        ["theBeach", "theBigSpot"],
        ["blackmat", "brian.123"]
    ]
    
AP_password =  "esp8266*"  # 8 char. if blank string, no ap will run
# (changes may require hardware reset not just soft reset)
    
##### For TIME:
timezone  = const(10)
ntpserver = "au.pool.ntp.org"
ntpserver2 = "3.pool.ntp.org"

##### For Blynk:
Token = "---------------------"  # Blynk
BlynkExtras = False    #  =  tweet, email, property, sync. lcd 1280 b
BlynkBridge = False    # 1280b
BlynkGpioAuto = False   # 1260 b

##### Thingspeak 
APIKEY = "----------------------------" # thingspeak

##### MQTT

##### For i2c:
sda = const(4) # D2
scl = const(5) # D1
oledtype = (64, 48) # D1-mini 64x48.  Regular "0.96inch" 128x64

##### Project file:
project = "P2a_customgpio"

'''
# alternative pin names, eg can use D0 instead of 16
D0=const(16);D1=const(5);D2=const(4);D3=const(0);D4=const(2)
D5=const(14);D6=const(12);D7=const(13);D8=const(15)

'''
