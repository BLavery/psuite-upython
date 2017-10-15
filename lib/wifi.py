
import network, time,  settings
import webrepl
wlan = network.WLAN(0)
ap = network.WLAN(1)

def setup_network():
        if settings.AP_password == "":
            ap.active(False)
        else:
            ap.active(True)  
            ap.config(essid = "ESP-"+str(int(ap.config("mac")[4]))+str(int(ap.config("mac")[5])), 
                      password = settings.AP_password)
            print("Own AP: '" + ap.config("essid") + "' pw: '"+settings.AP_password+"'")
        
        if wlan.isconnected():
            print("Wifi auto-reconnected") # no way to read router/station name??
        else:
            # scan what’s available
            available_networks = {}
            for network in wlan.scan():
                nw=network[0].decode("utf-8")
                print("Visible network:",nw)
                available_networks[nw] = network[1:]

            # Go over the preferred networks that are available, attempting first items or moving on if n/a
            for preference in [p for p in settings.known_networks if p[0] in available_networks]:
                    print("connecting to {0}...".format(preference[0]))
                    if connect_to(network_ssid=preference[0], password=preference[1]):
                        break  # We are connected so don't try more

        if wlan.isconnected():
            print("... client connection as" , wlan.config("dhcp_hostname"), wlan.ifconfig()[0])
            #print("... client connection as" ,  wlan.ifconfig()[0])
            return True
        return False

def connect_to(network_ssid: str, password: str) :
        wlan.connect(network_ssid, password)

        for check in range(0, 48):  # Wait a maximum of 12secs for success
            if wlan.isconnected():
                return True
            time.sleep_ms(250)
        return False

setup_network()
webrepl.start()

