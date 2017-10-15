


import ustruct as struct
import utime, machine, settings, socket, network
Rtc=machine.RTC()

def asctime():  # get human readable version
    x=utime.localtime()
    return '%02d/%02d/%04d %02d:%02d' % (x[2],x[1],x[0],x[3],x[4])
    # like 13/12/2017 14:31

if network.WLAN(0).isconnected():

    # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60  - and correct for timezone
    NTP_DELTA = 3155673600  - 3600*settings.timezone         


    def _getntptime(svr):
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1b
        try:
            addr = socket.getaddrinfo(svr, 123)[0][-1]
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(5)
            res = s.sendto(NTP_QUERY, addr)
            msg = s.recv(48)
            s.close()
            val = struct.unpack("!I", msg[40:44])[0]
            return val - NTP_DELTA
        except:
            return 0

    def _settime():
        t = _getntptime(settings.ntpserver)
        if t==0:
            t = _getntptime(settings.ntpserver2)  # attempt twice
        if t != 0:
            tm = utime.localtime(t) # format number into dmy ms etc
            tm = tm[0:3] + (0,) + tm[3:6] + (0,) # reformat to suit rtc
            Rtc.datetime(tm) # write into rtc
            print("Time sync:",asctime())
        else:
            print("Time sync fail")
        return (t != 0)
        
    if not _settime():  # first pass: immediate timesync. 
        utime.sleep(10)
        _settime() # and another go


    _tmr=machine.Timer(-1)
    _tmr.init(period=10800000, mode=machine.Timer.PERIODIC, callback=lambda t: _settime()) # resync every 3 hours

