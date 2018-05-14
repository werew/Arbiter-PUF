#!/usr/bin/env python3

from gevent.server import StreamServer
from gevent import sleep
import ssl

SLEEP = 0.5
PORT = 10000


def onoff(socket, address):
    print('New connection from %s:%s' % address)
    socket = ssl.wrap_socket(socket,server_side=True,certfile="cert.pem",keyfile="cert.pem")
    try:
        while(True):
            socket.sendall(b'0')
            sleep(SLEEP)
            socket.sendall(b'1')
            sleep(SLEEP)
    except ConnectionError:
        print('Closing connection to %s:%s' % address)
        socket.close()


if __name__ == '__main__':
    server = StreamServer(('0.0.0.0', PORT), onoff)
    print('Starting server')
    server.serve_forever()
