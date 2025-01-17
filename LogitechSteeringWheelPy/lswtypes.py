import ctypes
from ctypes import c_bool, c_int, c_byte, c_uint
from dataclasses import dataclass
from enum import Enum


class CControllerProperties(ctypes.Structure):
    _fields_ = [
        ('forceEnable', c_bool),
        ('overallGain', c_int),
        ('springGain', c_int),
        ('damperGain', c_int),
        ('defaultSpringEnabled', c_bool),
        ('defaultSpringGain', c_int),
        ('combinePedals', c_bool),
        ('wheelRange', c_int),
        ('gameSettingsEnabled', c_bool),
        ('allowGameSettings', c_bool),
    ]


@dataclass
class ControllerProperties:
    force_enable: bool
    overall_gain: int
    spring_gain: int
    damper_gain: int
    default_spring_enabled: bool
    default_spring_gain: int
    combine_pedals: bool
    wheel_range: int
    game_settings_enabled: bool
    allow_game_settings: bool

    def as_c_struct(self):
        c_struct = CControllerProperties()

        c_struct.forceEnable = c_bool(self.force_enable)
        c_struct.overallGain = c_int(self.overall_gain)
        c_struct.springGain = c_int(self.spring_gain)
        c_struct.damperGain = c_int(self.damper_gain)
        c_struct.defaultSpringEnabled = c_bool(self.default_spring_enabled)
        c_struct.defaultSpringGain = c_int(self.default_spring_gain)
        c_struct.combinePedals = c_bool(self.combine_pedals)
        c_struct.wheelRange = c_int(self.wheel_range)
        c_struct.gameSettingsEnabled = c_bool(self.game_settings_enabled)
        c_struct.allowGameSettings = c_bool(self.allow_game_settings)

        return c_struct

    @staticmethod
    def from_c_struct(c_struct: CControllerProperties):
        new_properties = ControllerProperties(
            force_enable=c_struct.forceEnable.value,
            overall_gain=c_struct.overallGain.value,
            spring_gain=c_struct.springGain.value,
            damper_gain=c_struct.damperGain.value,
            default_spring_enabled=c_struct.defaultSpringEnabled.value,
            default_spring_gain=c_struct.defaultSpringGain.value,
            combine_pedals=c_struct.combinePedals.value,
            wheel_range=c_struct.wheelRange.value,
            game_settings_enabled=c_struct.gameSettingsEnabled.value,
            allow_game_settings=c_struct.allowGameSettings.value
        )
        return new_properties


class CDIJOYSTATE2(ctypes.Structure):
    _fields_ = [
        ('lX', c_int),
        ('lY', c_int),
        ('lZ', c_int),
        ('lRx', c_int),
        ('lRy', c_int),
        ('lRz', c_int),
        ('rglSlider', c_int * 2),
        ('rgdwPOV', c_uint * 4),
        ('rgbButtons', c_byte * 128),
        ('lVX', c_int),
        ('lVY', c_int),
        ('lVZ', c_int),
        ('lVRx', c_int),
        ('lVRy', c_int),
        ('lVRz', c_int),
        ('rglVSlider', c_int * 2),
        ('lAX', c_int),
        ('lAY', c_int),
        ('lAZ', c_int),
        ('lARx', c_int),
        ('lARy', c_int),
        ('lARz', c_int),
        ('rglASlider', c_int * 2),
        ('lFX', c_int),
        ('lFY', c_int),
        ('lFZ', c_int),
        ('lFRx', c_int),
        ('lFRy', c_int),
        ('lFRz', c_int),
        ('rglFSlider', c_int * 2),
    ]


@dataclass
class DIJOYSTATE2:
    lX: int
    lY: int
    lZ: int
    lRx: int
    lRy: int
    lRz: int
    rglSlider: list
    rgdwPOV: list
    rgbButtons: list
    lVX: int
    lVY: int
    lVZ: int
    lVRx: int
    lVRy: int
    lVRz: int
    rglVSlider: list
    lAX: int
    lAY: int
    lAZ: int
    lARx: int
    lARy: int
    lARz: int
    rglASlider: list
    lFX: int
    lFY: int
    lFZ: int
    lFRx: int
    lFRy: int
    lFRz: int
    rglFSlider: list

    def as_c_struct(self):
        c_struct = CDIJOYSTATE2()

        c_struct.lX = self.lX
        c_struct.lY = self.lY
        c_struct.lZ = self.lZ
        c_struct.lRx = self.lRx
        c_struct.lRy = self.lRy
        c_struct.lRz = self.lRz

        for index, item in enumerate(self.rglSlider):
            c_struct.rglSlider[index] = ctypes.c_long(item)

        for index, item in enumerate(self.rgdwPOV):
            c_struct.rgdwPOV[index] = item

        for index, item in enumerate(self.rgbButtons):
            c_struct.rgbButtons[index] = item

        c_struct.lVX = self.lVX
        c_struct.lVY = self.lVY
        c_struct.lVZ = self.lVZ
        c_struct.lVRx = self.lVRx
        c_struct.lVRy = self.lVRy
        c_struct.lVRz = self.lVRz

        for index, item in enumerate(self.rglVSlider):
            c_struct.rglVSlider[index] = item

        c_struct.lAX = self.lAX
        c_struct.lAY = self.lAY
        c_struct.lAZ = self.lAZ
        c_struct.lARx = self.lARx
        c_struct.lARy = self.lARy
        c_struct.lARz = self.lARz

        for index, item in enumerate(self.rglASlider):
            c_struct.rglASlider[index] = item

        c_struct.lFX = self.lFX
        c_struct.lFY = self.lFY
        c_struct.lFZ = self.lFZ
        c_struct.lFRx = self.lFRx
        c_struct.lFRy = self.lFRy
        c_struct.lFRz = self.lFRz

        for index, item in enumerate(self.rglFSlider):
            c_struct.rglFSlider[index] = item

        return c_struct

    @staticmethod
    def from_c_struct(c_struct: CDIJOYSTATE2):
        rglSlider = list(c_struct.rglSlider)
        rgdwPOV = list(c_struct.rgdwPOV)
        rgbButtons = list(c_struct.rgbButtons)
        rglVSlider = list(c_struct.rglVSlider)
        rglASlider = list(c_struct.rglASlider)
        rglFSlider = list(c_struct.rglFSlider)

        new_state = DIJOYSTATE2(
            lX=c_struct.lX,
            lY=c_struct.lY,
            lZ=c_struct.lZ,
            lRx=c_struct.lRx,
            lRy=c_struct.lRy,
            lRz=c_struct.lRz,
            rglSlider=rglSlider,
            rgdwPOV=rgdwPOV,
            rgbButtons=rgbButtons,
            lVX=c_struct.lVX,
            lVY=c_struct.lVY,
            lVZ=c_struct.lVZ,
            lVRx=c_struct.lVRx,
            lVRy=c_struct.lVRy,
            lVRz=c_struct.lVRz,
            rglVSlider=rglVSlider,
            lAX=c_struct.lAX,
            lAY=c_struct.lAY,
            lAZ=c_struct.lAZ,
            lARx=c_struct.lARx,
            lARy=c_struct.lARy,
            lARz=c_struct.lARz,
            rglASlider=rglASlider,
            lFX=c_struct.lFX,
            lFY=c_struct.lFY,
            lFZ=c_struct.lFZ,
            lFRx=c_struct.lFRx,
            lFRy=c_struct.lFRy,
            lFRz=c_struct.lFRz,
            rglFSlider=rglFSlider
        )

        return new_state


class ForceType(Enum):
    NONE = -1
    SPRING = 0
    CONSTANT = 1
    DAMPER = 2
    SIDE_COLLISION = 3
    FRONTAL_COLLISION = 4
    DIRT_ROAD = 5
    BUMPY_ROAD = 6
    SLIPPERY_ROAD = 7
    SURFACE_EFFECT = 8
    SOFTSTOP = 10
    CAR_AIRBORNE = 11


class PeriodicSurfaceEffect(Enum):
    NONE = -1
    SINE = 0
    SQUARE = 1
    TRIANGLE = 2


class DeviceType(Enum):
    NONE = -1
    WHEEL = 0
    JOYSTICK = 1
    GAMEPAD = 2
    OTHER = 3


class Manufacurer(Enum):
    NONE = -1
    LOGITECH = 0
    MICROSOFT = 1
    OTHER = 2


class Model(Enum):
    G27 = 0
    DRIVING_FORCE_GT = 1
    G25 = 2
    MOMO_RACING = 3
    MOMO_FORCE = 4
    DRIVING_FORCE_PRO = 5
    DRIVING_FORCE = 6
    NASCAR_RACING_WHEEL = 7
    FORMULA_FORCE = 8
    FORMULA_FORCE_GP = 9
    FORCE_3D_PRO = 10
    EXTREME_3D_PRO = 11
    FREEDOM_24 = 12
    ATTACK_3 = 13
    FORCE_3D = 14
    STRIKE_FORCE_3D = 15
    G940_JOYSTICK = 16
    G940_THROTTLE = 17
    G940_PEDALS = 18
    RUMBLEPAD = 19
    RUMBLEPAD_2 = 20
    CORDLESS_RUMBLEPAD_2 = 21
    CORDLESS_GAMEPAD = 22
    DUAL_ACTION_GAMEPAD = 23
    PRECISION_GAMEPAD_2 = 24
    CHILLSTREAM = 25
    G29 = 26
    G920 = 27
