import ctypes
import sys
import time
import socket
import pygetwindow as gw

import logitech_steering_wheel as lsw

HOST = "169.254.100.16"
PORT = 8000
'''
class DIJOYSTATE2(ctypes.Structure):
    _fields_ = [
        ('lX', ctypes.c_int),
        ('lY', ctypes.c_int),
        ('lZ', ctypes.c_int),
        ('lRx', ctypes.c_int),
        ('lRy', ctypes.c_int),
        ('lRz', ctypes.c_int),
        ('rglSlider', ctypes.c_int * 2),
        ('rgdwPOV', ctypes.c_uint * 4),
        ('rgbButtons', ctypes.c_byte * 128),
        ('lVX', ctypes.c_int),
        ('lVY', ctypes.c_int),
        ('lVZ', ctypes.c_int),
        ('lVRx', ctypes.c_int),
        ('lVRy', ctypes.c_int),
        ('lVRz', ctypes.c_int),
        ('rglVSlider', ctypes.c_int * 2),
        ('lAX', ctypes.c_int),
        ('lAY', ctypes.c_int),
        ('lAZ', ctypes.c_int),
        ('lARx', ctypes.c_int),
        ('lARy', ctypes.c_int),
        ('lARz', ctypes.c_int),
        ('rglASlider', ctypes.c_int * 2),
        ('lFX', ctypes.c_int),
        ('lFY', ctypes.c_int),
        ('lFZ', ctypes.c_int),
        ('lFRx', ctypes.c_int),
        ('lFRy', ctypes.c_int),
        ('lFRz', ctypes.c_int),
        ('rglFSlider', ctypes.c_int * 2),
    ]
'''

def connect():
    hwnd = gw.getActiveWindow()._hWnd
    initialized = lsw.initialize_with_window(True, hwnd)

    if initialized:
        print('initialized successfully')
    else:
        print('initialization failed')
        return

    if lsw.is_connected(0):
        print('connected to a steering wheel at index 0')
        
    lsw.update()
    print(lsw.get_current_controller_properties(0))

def main():
    connect()
    #state = DIJOYSTATE2(lX=-4, lZ=7)
    i = 0
    while(1):
        i += 1
        lsw.update()
        state = lsw.get_c_state(0)
        print("Transmit ", state.lX)
        pdata = ctypes.string_at(ctypes.byref(state), ctypes.sizeof(state))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(pdata, (HOST, PORT))
        time.sleep(1)

        
if __name__ == '__main__':
    main()
