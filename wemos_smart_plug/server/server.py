#!/usr/bin/env python3

from gevent.server import StreamServer
from gevent import sleep
import json
import hashlib
import struct

SLEEP = 0.5
PORT = 10000

SECRET = b"43993478947239474234823942398472394732984723"
MAX_CHALLS = 4

def readline(socket):
    line = b""
    for _ in range(1024):
        c = socket.recv(1)
        line += c
        if c == b"\n": 
            return line.decode("utf-8") 




class Chall_Factory:
    def __init__(self,max_challs):
        self.max_challs = max_challs
        self.challs = []

    def gen_chall(self):
        chall = urandom.getrandbits(32)
        self.challs.append(chall)
        if len(self.chall) > self.max_challs:
            self.chall.pop(0)

        return chall

    def verify(self,chall):
        return chall in self.challs

    def verify_and_rm(self,chall):
        if self.verify(chall):
            self.challs.remove(chall)
            return True
        return False

def gen_otp(action,chall):
    a = action.encode("utf-8")
    c = struct.pack(">I",chall)
    h = hashlib.sha256(SECRET+a+c)
    return h.hexdigest()


    

def turn_on(socket):
    socket.sendall(b'{"action":"genchall"}\n')  
    response = json.loads(readline(socket))
    otp = gen_otp("on",response["chall"])
    msg  = json.dumps({"action": "on", "chall": response["chall"], "otp": otp})+"\n"
    socket.sendall(msg.encode("utf-8"))

def turn_off(socket):
    socket.sendall(b'{"action":"genchall"}\n')  
    response = json.loads(readline(socket))
    otp = gen_otp("off",response["chall"])
    msg  = json.dumps({"action": "off", "chall": response["chall"], "otp": otp})+"\n"
    socket.sendall(msg.encode("utf-8"))



def onoff(socket, address):

    print('New connection from %s:%s' % address)
    socket.settimeout(5)
    cf = Chall_Factory(MAX_CHALLS)

    while(True):
        try:
            turn_on(socket)
            sleep(SLEEP)
            turn_off(socket)
            sleep(SLEEP)


        except Exception as e:
            print(e)
            print('Closing connection to %s:%s' % address)
            socket.close()
            return


if __name__ == '__main__':
    server = StreamServer(('0.0.0.0', PORT), onoff)
    print('Starting server')
    server.serve_forever()
