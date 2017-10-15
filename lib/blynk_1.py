import socket, errno
import ustruct as struct
import utime as time

from blynk_0 import *

def idle_loop (self, start, delay): 
    # 200 Hz loop
    if self._on_tick: 
        self._tick_count = 1 + self._tick_count
        if self._tick_count == self._tick_scale:
            self._tick_count = 0
            rtn=self._on_tick(self._tick_state)
            if rtn != None:
                self._tick_state = rtn
    while (time.ticks_ms()-start) < delay:
        pass
    return start + delay

def _format_msg(self, msg_type, *args):
    data = bytes('\0'.join(map(str, args)), 'ascii') 
    return struct.pack(HDR_FMT, msg_type, self._new_msg_id(), len(data)) + data

def _handle_hw(self, data):
    params = list(map(lambda x: x.decode('ascii'), data.split(b'\0'))) 
    cmd = params.pop(0)
    if cmd == 'pm':
        if self._on_setup:
            self._on_setup(params)
        self._pins_configured = True
    elif cmd == 'vw':
        pin = int(params.pop(0))
        if pin in self._vr_pins and self._vr_pins[pin].write:
            self._vr_pins[pin].write(params, pin, self._vr_pins[pin].state)
    elif cmd == 'vr':
        pin = int(params.pop(0))
        if pin in self._vr_pins and self._vr_pins[pin].read:
            val = self._vr_pins[pin].read(pin, self._vr_pins[pin].state)
            if val != None : 
                self.virtual_write(pin, val)
    elif self._pins_configured:
        if cmd == 'dw':
            pin = int(params.pop(0))
            val = int(params.pop(0))
            if pin in self._digital_hw_pins:
                if self._digital_hw_pins[pin].write is not None:
                    self._digital_hw_pins[pin].write(val, pin, self._digital_hw_pins[pin].state)

        elif cmd == 'dr':
            pin = int(params.pop(0))
            if pin in self._digital_hw_pins:
                if self._digital_hw_pins[pin].read is not None:
                    val = self._digital_hw_pins[pin].read(pin, self._digital_hw_pins[pin].state)
                    if val != None:   
                        self._send(self._format_msg(MSG_HW, 'dw', pin, val))

        #else:
        #    raise ValueError("Unknown message cmd: %s" % cmd)

def _new_msg_id(self):
    self._msg_id += 1
    if (self._msg_id > 0xFFFF):
        self._msg_id = 1
    return self._msg_id

def _settimeout(self, timeout):
    if timeout != self._timeout:
        self._timeout = timeout
        self.conn.settimeout(timeout)


def _recv(self, length, timeout=0):

    self._settimeout(timeout)
    try:
        self._rx_data += self.conn.recv(length)
    except OSError as e:
        if e.args[0] == errno.EAGAIN or e.args[0] == errno.ETIMEDOUT:
            return b''
        else:
            print("RX Error")
            self._must_close = True
            return b''
         
            
    if len(self._rx_data) >= length:
        data = self._rx_data[:length]
        self._rx_data = self._rx_data[length:]
        return data
    else:
        return b''


def _sendL(self, data, send_anyway):  # locked
    if self._tx_count < MAX_MSG_PER_SEC or send_anyway:
        retries = 0
        while retries <= MAX_TX_RETRIES:
            try:
                
                self.conn.send(data)
                self._tx_count += 1
                
                break
                
            except OSError as er:
                if er.args[0] != errno.EAGAIN:
                    print(er)
                    return False
                else:
                    time.sleep_ms(RE_TX_DELAY)
                    retries += 1
        return True

def _send(self, data, send_anyway=False):
    #self.lock.acquire()  # lock against reentrancy - no longer reqd
    was_sent = self._sendL(data, send_anyway)
    #self.lock.release()
    if not was_sent:
        print("Send Error")
        self._must_close = True
    
def _close(self, emsg=None):
    self.conn.close()
    self._rx_data = b''
    self._failed_pings = 0   
    if emsg:
        print('[closed] ' , emsg)
    if self.state == AUTHENTICATED: 
        if self._on_disconnect:
            self._on_disconnect()
    self.state = DISCONNECTED
    time.sleep(RECONNECT_DELAY)

def _server_alive(self):
    c_time = int(time.time())
    if self._m_time != c_time: # 1/sec
        self._m_time = c_time
        self._tx_count = 0
        
        if c_time - self._hb_time >= HB_PERIOD and self.state == AUTHENTICATED:
            # time to issue another heartbeat ping
            if self._last_hb_id != 0:    
                self._failed_pings += 1
                print("PING unanswered" + str(self._failed_pings))
                if self._failed_pings > 1:  # 2 strikes & y're OUT
                    return False
            self._hb_time = c_time
            self._last_hb_id = self._new_msg_id()
            self._send(struct.pack(HDR_FMT, MSG_PING, self._last_hb_id, 0), True)
    return True

