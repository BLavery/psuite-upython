import socket
import ustruct as struct
import utime as time

from blynk_0 import *


def run(self):

    #Run the Blynk client (blocking mode)

    self._start_time = time.ticks_ms()
    self._task_millis = self._start_time # nyi
    self._rx_data = b''
    self._msg_id = 1
    self._pins_configured = False
    self._timeout = -1
    self._tx_count = 0
    self._m_time = 0
    self._must_close = False
    

    while True:  # loop forever
        self._must_close = False
        while self.state != AUTHENTICATED:
            if self._do_connect:
                try:
                    self.state = CONNECTING
                    print('TCP: Connecting to' , self._server, self._port)
                    self.conn = socket.socket()
                    self.conn.connect(socket.getaddrinfo(self._server, self._port)[0][4])
                except:
                    self._close('Fail to connect')
                    continue


                self.state = AUTHENTICATING
                hdr = struct.pack(HDR_FMT, MSG_LOGIN, self._new_msg_id(), len(self._token))
                print('authenticating...')
                self._send(hdr + self._token, True)
                data = self._recv(HDR_LEN, timeout=MAX_SOCK_TO)
                if not data:
                    self._close('Authentication t/o')
                    continue

                msg_type, msg_id, status = struct.unpack(HDR_FMT, data)
                if status != STA_SUCCESS or msg_id == 0:
                    self._close('Authentication fail')
                    continue

                self.state = AUTHENTICATED
                self._send(self._format_msg(MSG_HW_INFO, "h-beat", HB_PERIOD, 'dev', 'esp', "cpu", "8266"))
                print('Blynk Access.')
                if self._on_connect:
                    self._on_connect()
                self._start_time = time.ticks_ms()  
            else:
                self._start_time = self.idle_loop(self._start_time, TASK_PERIOD_RES)

        self._hb_time = 0
        self._last_hb_id = 0
        self._tx_count = 0
        self._must_close = False
        while self._do_connect:
            data = self._recv(HDR_LEN, NON_BLK_SOCK)
            if data:
                msg_type, msg_id, msg_len = struct.unpack(HDR_FMT, data)
                if msg_id == 0:
                    pass
                if msg_type == MSG_RSP:
                    if msg_id == self._last_hb_id:
                        self._last_hb_id = 0
                        self._failed_pings = 0   
                elif msg_type == MSG_PING:
                    self._send(struct.pack(HDR_FMT, MSG_RSP, msg_id, STA_SUCCESS), True)
                elif msg_type == MSG_HW or msg_type == MSG_BRIDGE:
                    data = self._recv(msg_len, MIN_SOCK_TO)
                    if data:

                        self._handle_hw(data)
                else:
                    self._close('unknown msg ', msg_type)
                    break
            else:
                self._start_time = self.idle_loop(self._start_time, IDLE_TIME_MS)
            if not self._server_alive():
                self._close('Server off')
                break
            if self._must_close:
                self._close('Network err')
                break
                


        if not self._do_connect:
            self._close()
            print('Blynk discon req')

