#!/usr/bin/env python3

from gevent.server import StreamServer
from gevent import sleep
import json
import hashlib
import struct

SLEEP = 0.5
PORT = 10000
SECRET = b"43993478947239474234823942398472394732984723" # Secret shared key

def readline(socket):
    """Reads up to 1024 chars until a newline is encountered.
    Returns an utf-8 string or None if no newline was found.
    """
    line = b""
    for _ in range(1024):
        c = socket.recv(1)
        line += c
        if c == b"\n": 
            return line.decode("utf-8") 


def gen_otp(action,chall):
    """Generate a OneTimePass given an action and a challenge"""
    a = action.encode("utf-8")
    c = struct.pack(">I",chall)
    h = hashlib.sha256(SECRET+a+c)

    h1 = hashlib.sha256(SECRET+a+c)
    h2 = hashlib.sha256(SECRET+h1.digest())
    return h2.hexdigest()

    
def turn_on(socket):
    """Asks for a challenge and sends an authenticated turn on request """

    # Get new challenge
    socket.sendall(b'{"action":"genchall"}\n')  
    response = json.loads(readline(socket))

    # Generate request
    otp = gen_otp("on",response["chall"])
    msg  = json.dumps({"action": "on", "chall": response["chall"], "otp": otp})+"\n"
    socket.sendall(msg.encode("utf-8"))


def turn_off(socket):
    """Asks for a challenge and sends an authenticated turn off request """
    
    # Get a new challenge
    socket.sendall(b'{"action":"genchall"}\n')  
    response = json.loads(readline(socket))

    # Generate request
    otp = gen_otp("off",response["chall"])
    msg  = json.dumps({"action": "off", "chall": response["chall"], "otp": otp})+"\n"
    socket.sendall(msg.encode("utf-8"))



def onoff(socket, address):

    print('New connection from %s:%s' % address)
    socket.settimeout(5)

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
