
from micropython import const

HDR_LEN = const(5)
HDR_FMT = "!BHH"

MAX_MSG_PER_SEC = const(20)

MSG_RSP = const(0)
MSG_LOGIN = const(2)
MSG_PING = const(6)
MSG_TWEET = const(12)
MSG_EMAIL = const(13)
MSG_NOTIFY = const(14)
MSG_BRIDGE = const(15)
MSG_HW_SYNC = const(16)
MSG_HW_INFO = const(17)
MSG_PROPERTY = const(19)
MSG_HW = const(20)

STA_SUCCESS = const(200)

HB_PERIOD = const(10)
NON_BLK_SOCK = const(0)
MIN_SOCK_TO = const(1)  # 1 second
MAX_SOCK_TO = const(5)  # 5 seconds
RECONNECT_DELAY = const(2)  # 1 second
TASK_PERIOD_RES = const(50)  # 50 ms
IDLE_TIME_MS = const(5)  # 5 ms

RE_TX_DELAY = const(2)
MAX_TX_RETRIES = const(3)

MAX_VIRTUAL_PINS = const(32)

DISCONNECTED = const(0)
CONNECTING = const(1)
AUTHENTICATING = const(2)
AUTHENTICATED = const(3)



