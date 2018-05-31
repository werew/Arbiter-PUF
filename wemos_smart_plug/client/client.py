
# Indicates wether the code is running on the board
# set it to True before flashing it
__esp8266__ = False

import usocket
import machine
import ussl
import ujson
import urandom
import uhashlib
import ustruct
import ubinascii
if __esp8266__: import network



SERVER_NAME = "192.168.150.199"
SERVER_NAME = "0.0.0.0"
#SERVER_NAME = "192.168.2.24"
SERVER_PORT = 10000
WIFI_SSID = "esp8266"
WIFI_SSID = "Wifi282-1"
WIFI_PSK = "twente2018"
WIFI_PSK = "WiFi28201!"
MAX_CHALLS = 4


SECRET= b"43993478947239474234823942398472394732984723"



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
    return sock

def turn_on():
    if __esp8266__: machine.Pin(2, machine.Pin.OUT).off()
    print("On")

def turn_off():
    if __esp8266__: machine.Pin(2, machine.Pin.OUT).on()
    print("Off")


def gen_otp(action,chall):
    a = action.encode("utf-8")
    c = ustruct.pack(">I",chall)
    h = uhashlib.sha256(SECRET+a+c)
    return ubinascii.hexlify(h.digest()).decode("utf-8")


class Chall_Factory:
    def __init__(self,max_challs):
        self.max_challs = max_challs
        self.challs = [] 

    def gen_chall(self):
        chall = urandom.getrandbits(32)
        self.challs.append(chall)
        if len(self.challs) > self.max_challs:
            self.challs.pop(0)

        return chall

    def verify(self,chall):
        return chall in self.challs

    def verify_and_rm(self,chall):
        if self.verify(chall):
            self.challs.remove(chall)
            return True
        return False

def main():

    if __esp8266__: connect_to_wifi()
    s = connect_to_server()

    cf = Chall_Factory(MAX_CHALLS)
    while True:
        try:
            l = s.readline()
            print(l)
            if len(l) == 0: return
            cmd = ujson.loads(l)
        
            if cmd['action'] == "genchall":
                s.send('{"chall":'+str(cf.gen_chall())+'}\n')

            elif cmd['action'] == "on":
                if cf.verify_and_rm(cmd['chall']) and \
                   gen_otp(cmd["action"],cmd["chall"]) == cmd["otp"]:
                        turn_on()
                else: 
                    print("Command refused")

            elif cmd['action'] == "off":
                if cf.verify_and_rm(cmd['chall']) and \
                   gen_otp(cmd["action"],cmd["chall"]) == cmd["otp"]:
                        turn_off()
                else: 
                    print("Command refused")

            else:
                print("Invalid action")

        except Exception as e:
            print(e)
            continue
        

main()

