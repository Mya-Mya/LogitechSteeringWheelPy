import ctypes
import sys
import time
import socket

from PyQt5 import QtGui, QtWidgets, QtCore

import logitech_steering_wheel as lsw

HOST = "169.254.100.16"
PORT = 8000

class MyMainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.update_timer = QtCore.QTimer()
        self.update_timer.setInterval(30)
        self.update_timer.setSingleShot(False)
        self.update_timer.timeout.connect(self._update_sw)

        self.connect_button = QtWidgets.QPushButton('connect')
        self.current_angle = QtWidgets.QSpinBox()
        self.current_angle.setMaximum(2147483647)
        self.current_angle.setMinimum(-2147483648)
        self.stop_button = QtWidgets.QPushButton('stop')
        self.effect_button = QtWidgets.QPushButton('Toggle feedback')

        self.connect_button.clicked.connect(self.connect_to_wheel)
        self.stop_button.clicked.connect(self.stop)
        self.effect_button.clicked.connect(self.toggle_feedback)

        layout = QtWidgets.QVBoxLayout()
        widget = QtWidgets.QWidget()

        widget.setLayout(layout)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.effect_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.current_angle)

        self.setCentralWidget(widget)

    def connect_to_wheel(self) -> None:
        w = self.winId()
        initialized = lsw.initialize_with_window(True, w)

        if initialized:
            print('initialized successfully')
        else:
            return

        if lsw.is_connected(0):
            print('connected to a steering wheel at index 0')
            self.update_timer.start()

        lsw.update()
        print(lsw.get_current_controller_properties(0))

    def _update_sw(self):
        lsw.update()
        state = lsw.get_state(0)
        state_c = lsw.get_c_state(0)
        pdata = ctypes.string_at(ctypes.byref(state_c), ctypes.sizeof(state_c))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(pdata, (HOST, PORT))
        
        self.current_angle.setValue(state.lX)
        if (state.lX > 4000):
            force = min(99, max(0, ((state.lX - 4000)/100)))
        else:
            force = max(-99, min(0, ((state.lX + 4000)/100)))

        print("Force ", force)
        lsw.play_constant_force(0, int(force))

    def toggle_feedback(self):
        if lsw.is_playing(0, lsw.ForceType.BUMPY_ROAD):
            lsw.stop_bumpy_road_effect(0)
        else:
            lsw.play_bumpy_road_effect(0, 20)

    def stop(self):
        print('disconnecting')
        lsw.shutdown()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.stop()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainwindow()
    window.show()
    sys.exit(app.exec_())
