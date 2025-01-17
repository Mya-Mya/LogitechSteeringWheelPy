from .lswtypes import *
from .gateway import *
from datetime import datetime
from math import radians


class G29:
    def __init__(self, index: int):
        """
        Before using this class, make sure...

        1. You have already loaded the DLL file, i.e.,

        ```python
        import LogitechSteeringWheelPy as lsw
        lsw.load_dll("Path to the DLL File")
        ```

        2. You have already obtained the window id of GUI framework you are using, i.e.,

        ```python
        hwnd = Window ID Obtaining Function of GUI Framework you are Using.
        ```

        3. You have already initialized the SDK, i.e.,

        ```python
        initialized = lsw.initialize_with_window(True, hwnd)
        assert initialized
        ```

        """
        self.index = index
        self.state:DIJOYSTATE2 = None
        self.steering_range_rad = .0
        self.steering_rad = .0
        self.throttle_normalized = .0
        self.brake_normalized = .0
        self.updated_at = datetime.now()

    def update(self):
        """
        Note that this function should be called JUST ONCE per frame of your game.
        """
        update()
        self.state = get_state(self.index)
        steering_range, _ = get_operating_range(self.index)

        self.steering_range_rad = radians(steering_range)
        self.steering_rad = - self.state.lX / 65536 * self.steering_range_rad
        self.throttle_normalized = 1 - (self.state.lY + 32768) / 65535
        self.brake_normalized = 1 - (self.state.lRz + 32768) / 65535
        self.updated_at = datetime.now()