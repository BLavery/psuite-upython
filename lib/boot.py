#This file is executed on every boot (including wake-boot from deepsleep)
print("Mem:",gc.mem_free())
import network
Wifi = network.WLAN(network.STA_IF)
Wifi.active(True) # allow auto reconnect






