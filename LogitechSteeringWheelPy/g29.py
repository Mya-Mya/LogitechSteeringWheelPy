from typing import Literal, Optional
from .lswtypes import *
from .gateway import *
from datetime import datetime
from math import radians
from enum import Enum


class G29:
    class Button(Enum):
        Up = "Up"
        Right = "Right"
        Down = "Down"
        Left = "Left"
        Circle = "Circle"
        Triangle = "Triangle"
        Square = "Square"
        Cross = "Cross"
        R2 = "R2"
        R3 = "R3"
        L2 = "L2"
        L3 = "L3"
        Plus = "Plus"
        Minus = "Minus"
        Share = "Share"
        Options = "Options"
        Playstation = "Playstation"
        Return = "Return"
        PaddleLeft = "PaddleLeft"
        PaddleRight = "PaddleRight"

    NONPOV_BUTTON_NUMBER = {
        Button.Circle: 2,
        Button.Triangle: 3,
        Button.Square: 1,
        Button.Cross: 0,
        Button.R2: 6,
        Button.R3: 10,
        Button.L2: 7,
        Button.L3: 11,
        Button.Plus: 19,
        Button.Minus: 20,
        Button.Share: 8,
        Button.Options: 9,
        Button.Playstation: 24,
        Button.Return: 23,
        Button.PaddleLeft: 4,
        Button.PaddleRight: 5,
    }

    POV_BUTTONS = {Button.Up, Button.Right, Button.Down, Button.Left}

    def __init__(self, index: int, positive_angle: Literal["counterclockwise", "clockwise"] = "counterclockwise"):
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
        self.positive_angle = positive_angle
        self.sgn_angle = {
            "counterclockwise": -1,
            "clockwise": +1
        }[positive_angle]
        self.state: DIJOYSTATE2 = None
        self.steering_range_rad = .0
        self.steering_rad = .0
        self.throttle_normalized = .0
        self.brake_normalized = .0
        self.updated_at = datetime.now()
        self.pressed_pov: Optional[G29.Button] = None

    def update(self):
        """
        Note that this function should be called JUST ONCE per frame of your game.
        """
        self.state = get_state(self.index)
        steering_range, _ = get_operating_range(self.index)

        self.steering_range_rad = radians(steering_range)
        self.steering_rad = self.sgn_angle * self.state.lX / 65536 * self.steering_range_rad
        self.throttle_normalized = 1 - (self.state.lY + 32768) / 65535
        self.brake_normalized = 1 - (self.state.lRz + 32768) / 65535
        self.updated_at = datetime.now()

        pov0 = self.state.rgdwPOV[0]
        if pov0 == 0:
            self.pressed_pov = G29.Button.Up
        elif pov0 == 9000:
            self.pressed_pov = G29.Button.Right
        elif pov0 == 18000:
            self.pressed_pov = G29.Button.Down
        elif pov0 == 27000:
            self.pressed_pov = G29.Button.Left
        else:
            self.pressed_pov = None

    def _is_pov_pressed(self, button: Button) -> bool:
        return self.pressed_pov is not None and button == self.pressed_pov

    def is_released(self, button: Button) -> bool:
        # POV
        if button in G29.POV_BUTTONS:
            raise NotImplementedError("`is_released` for POV buttons is not implemented")
        # Non-POV
        button_number = G29.NONPOV_BUTTON_NUMBER[button]
        return button_released(self.index, button_number)

    def is_triggered(self, button: Button) -> bool:
        # POV
        if button in G29.POV_BUTTONS:
            raise NotImplementedError("`is_triggered` for POV buttons is not implemented")
        # Non-POV
        button_number = G29.NONPOV_BUTTON_NUMBER[button]
        return button_triggered(self.index, button_number)

    def is_pressed(self, button: Button) -> bool:
        # POV
        if button in G29.POV_BUTTONS:
            return self._is_pov_pressed(button)
        # Non-POV
        button_number = G29.NONPOV_BUTTON_NUMBER[button]
        return button_is_pressed(self.index, button_number)
