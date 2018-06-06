
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
import utime
import ubinascii
if __esp8266__: import network



SERVER_NAME = "192.168.151.204"
SERVER_PORT = 10000
WIFI_SSID = "esp8266"
WIFI_PSK = "twente2018"


SECRET= b"43993478947239474234823942398472394732984723" # Secret shared key



def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PSK)
    while not sta_if.isconnected():
        pass

def connect_to_server():
    """Connects to the server and returns a socket"""
    addr_info = usocket.getaddrinfo(SERVER_NAME, SERVER_PORT)
    addr = addr_info[0][-1]
    sock = usocket.socket(usocket.AF_INET,  usocket.SOCK_STREAM)
    sock.connect(addr)
    return sock

def turn_on():
    if __esp8266__: machine.Pin(2, machine.Pin.OUT).on()
    print("On")

def turn_off():
    if __esp8266__: machine.Pin(2, machine.Pin.OUT).off()
    print("Off")


def gen_otp(action,chall):
    """Generate a OneTimePass given an action and a challenge"""
    a = action.encode("utf-8")
    c = ustruct.pack(">I",chall)
    h1 = uhashlib.sha256(SECRET+a+c)
    h2 = uhashlib.sha256(SECRET+h1.digest())
    return ubinascii.hexlify(h2.digest()).decode("utf-8")


class Chall_Factory:
    """An helper class to generate and verify challenges""" 
    def __init__(self):
        urandom.seed(int(utime.time()))

    def gen_chall(self):
        """Generates a returns a new challenge."""
        self.last_chall = urandom.getrandbits(32)
        return self.last_chall

    def verify_and_rm(self,chall):
        """Compares a chall with the last generated challege,
           this last is removed in case match
        """
        if self.last_chall == chall:
            self.last_chall == None
            return True
        return False



def main():

    if __esp8266__: connect_to_wifi()
    s = connect_to_server()

    cf = Chall_Factory()
    while True:
        try:

            #### Get command from the server ####
            l = s.readline()
            print(l)
            cmd = ujson.loads(l)
       
            ####   Match possible actions    ####

            if cmd['action'] == "genchall":
                # Send new challenge to the server
                s.send('{"chall":'+str(cf.gen_chall())+'}\n')


            elif cmd['action'] == "on":
                # If the message contains a valid otp, turn on the device
                if cf.verify_and_rm(cmd['chall']) and \
                   gen_otp(cmd["action"],cmd["chall"]) == cmd["otp"]:
                        turn_on()
                else: 
                    print("Command refused")


            elif cmd['action'] == "off":
                # If the message contains a valid otp, turn off the device
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


