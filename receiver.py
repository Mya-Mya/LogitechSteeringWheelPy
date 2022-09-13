import socket
import ctypes
from logitech_steering_wheel._state import DIJOYSTATE2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
HOST = "127.0.0.1"
PORT = 8000

sock.bind((HOST, PORT))

while True:
    data, addr = sock.recvfrom(ctypes.sizeof(DIJOYSTATE2))
    print("received msg: %s" % data)