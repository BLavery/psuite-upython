
from Oled import oled
from pblynk import Blynk
b=Blynk()




if oled:
    oled.fill(0)
    oled.text("Hello",0,0,1)
    oled.show()

def jlog(val, pin, st):
    if oled:
        oled.fill(0)
        oled.text(val[0],0,0,1) 
        oled.show()
    print(val[0])
b.add_virtual_pin(19, write= jlog)




######################################################################################

b.run()

######################################################################################



# At 8266:
# oled on i2c  
# 
# At APP:
# Terminal widget on V19. only interested in its input window

