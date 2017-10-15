from blynk_0 import *

def sync_all(self):
    if self.state == AUTHENTICATED:
        self._send(self._format_msg(MSG_HW_SYNC))

def sync_virtual(self, pin):
    if self.state == AUTHENTICATED:
        self._send(self._format_msg(MSG_HW_SYNC, 'vr', pin))

def tweet(self, msg):
    if self.state == AUTHENTICATED:
        self._send(self._format_msg(MSG_TWEET, msg))

def email(self, to, subject, body):
    if self.state == AUTHENTICATED:
        self._send(self._format_msg(MSG_EMAIL, to, subject, body))

def set_property(self, pin, prop, val):
    if self.state == AUTHENTICATED:
        if type(val) == type([]):  
            val = '\0'.join(map(str, val))  
        self._send(self._format_msg(MSG_PROPERTY,  pin, prop, val))

def lcd_print(self, vpin, x, y, msg):
    self.virtual_write(vpin,  [ "p", str(x%16), str(y%2),  msg])

def lcd_cls(self, vpin):  
    self.virtual_write(vpin, "clr")

