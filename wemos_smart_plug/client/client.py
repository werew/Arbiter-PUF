
# Indicates wether the code is running on the board
# set it to True before flashing it
__esp8266__ = False

import usocket
import machine
import ussl
if __esp8266__: import network



SERVER_NAME = "192.168.150.199"
SERVER_NAME = "0.0.0.0"
SERVER_NAME = "192.168.2.17"
SERVER_PORT = 10000
WIFI_SSID = "esp8266"
WIFI_SSID = "Wifi282-1"
WIFI_PSK = "twente2018"
WIFI_PSK = "WiFi28201!"



def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PSK)
    while not sta_if.isconnected():
        pass

def connect_to_server():
    addr_info = usocket.getaddrinfo(SERVER_NAME, SERVER_PORT)
    addr = addr_info[0][-1]
    sock = usocket.socket(usocket.AF_INET,  usocket.SOCK_STREAM)
    sock.connect(addr)
    sslsock = ussl.wrap_socket(sock)
    return sslsock

def turn_on():
    if __esp8266__: machine.Pin(2, machine.Pin.OUT).off()
    print("On")

def turn_off():
    if __esp8266__: machine.Pin(2, machine.Pin.OUT).on()
    print("Off")


if __esp8266__: connect_to_wifi()
s = connect_to_server()

while True:
    data = s.read(1)
    if (data == b'0'):
        turn_off()
    elif (data == b'1'):
        turn_on()
