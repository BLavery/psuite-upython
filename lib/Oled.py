from machine import I2C, Pin
import settings, network, sntp

oled=False
_i2c=I2C(-1, Pin(settings.scl), Pin(settings.sda))
if 60 in set(_i2c.scan()):
    import ssd1306
    oled=ssd1306.SSD1306_I2C(settings.oledtype[0],settings.oledtype[1],_i2c) # what pixels?
    _t=sntp.asctime()
    _ip=network.WLAN(network.STA_IF).ifconfig()[0]
    _dot2=_ip.index('.', _ip.index('.') + 1)
    # fits 64x48
    oled.text("pSuite",0,0,1)
    oled.text(_ip[0:_dot2+1] ,0,10,1)
    oled.text(_ip[_dot2+1:] ,6,20,1)
    oled.text(_t[11:],0,30,1) # time
    oled.text(_t[0:6]+_t[8:10],0,40,1) # date yy not yyyy (D1 mini oled)
    oled.show()

# better layout option for 128x64 display?

# see framebuf calls: oled uses those:  0=black 1=white
#     http://docs.micropython.org/en/latest/esp8266/library/framebuf.html#module-framebuf
