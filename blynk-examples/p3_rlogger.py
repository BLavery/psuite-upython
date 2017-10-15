

from Oled import oled
from pblynk import Blynk
import sntp, network
b=Blynk()



# rlogger

rlctr = 0   

def Tfunc(st):
    # write to (terminal style) rlogger at APP on vp 18    
    global rlctr
    rlctr = rlctr+1
    b.virtual_write(18, sntp.asctime()+ " "+str(rlctr) + "\n"); 
    print(sntp.asctime(), rlctr)
    
b.Ticker(Tfunc,1000) # 5 secs


def cnct_cb():
    print ("Connected: "+ sntp.asctime()[11:])
    b.virtual_write(18, "\n"+network.WLAN(0).config("dhcp_hostname")+"\n")
b.on_connect(cnct_cb)


######################################################################################

b.run()

######################################################################################


# At APP:
# make terminal widget on that V18, fill whole phone screen, 
# turn off its input box
# now it is a live-time remote log display screen rpi->app  with rlogger.write()
# but server WONT indefinitely buffer messages if APP is offline.

# OR use labelled value box
