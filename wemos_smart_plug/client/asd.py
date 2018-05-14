
# Indicates wether the code is running on the board
# set it to True before flashing it
__esp8266__ = False

import socket
import ssl



SERVER_NAME = "192.168.150.199"
SERVER_NAME = "0.0.0.0"
SERVER_PORT = 10000
WIFI_SSID = "esp8266"
WIFI_PSK = "twente2018"



def connect_to_server():
    addr_info = socket.getaddrinfo(SERVER_NAME, SERVER_PORT)
    addr = addr_info[0][-1]
    sock = socket.socket()
    sock.connect(addr)
    sslsock = ssl.wrap_socket(sock)
    return sslsock

def turn_on():
    print("On")

def turn_off():
    print("Off")


s = connect_to_server()

while True:
    data = s.recv(1)
    if (data == b'0'):
        turn_off()
    elif (data == b'1'):
        turn_on()
