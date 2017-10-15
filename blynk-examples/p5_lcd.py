
import settings
settings.BlynkExtras = True  # load the lcd functions
from pblynk import Blynk
import sntp
b=Blynk()



# lcd widget

ctr = 0   

def Tfunc(st):
    # write to (terminal style) rlogger at APP on vp 21    
    global ctr
    ctr = ctr+1
    b.lcd_cls(21)
    b.lcd_print(21, 0,0, sntp.asctime())
    b.lcd_print(21, 0,1,str(ctr)) 
    print(sntp.asctime(), ctr)
    
b.Ticker(Tfunc,1000) # 5 secs


######################################################################################

b.run()

######################################################################################


# At APP:
# make LCD V21,  


