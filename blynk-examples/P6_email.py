
import settings, sys, time
settings.BlynkExtras = True  # load the email functions
from pblynk import Blynk
import sntp
b=Blynk()



def cnct_cb():
    print ("Connected: "+ sntp.asctime())
    
    b.email("bl@blavery.com", "subject 44", "Test.  Body")   
    print("sent email via blynk server. nothing more to do in this demo. Exit!")
    time.sleep(3)
    sys.exit()
b.on_connect(cnct_cb)



######################################################################################

b.run()

######################################################################################

# At APP:
# nothing except put an email widget to screen.
