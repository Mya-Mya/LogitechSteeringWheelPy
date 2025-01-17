from typing import Union
from pathlib import Path
import ctypes
from ctypes import c_bool, c_int, c_int64, c_float, c_void_p, c_long, byref, pointer, POINTER, create_unicode_buffer
from .lswtypes import *

dll: ctypes.WinDLL = None


def load_dll(file: Union[str, Path], reload: bool = False):
    """Please specify the path for `LogitechSteeringWheelEnginesWrapper.dll`.
    """
    global dll
    if reload:
        dll = None
    if dll is not None:
        return
    if isinstance(file, Path):
        file = str(file)
    dll = ctypes.windll.LoadLibrary(file)
    dll.LogiSteeringInitialize.restype = c_bool
    dll.LogiSteeringInitializeWithWindow.restype = c_bool
    dll.LogiSteeringInitialize.restype = c_bool
    dll.LogiSteeringGetSdkVersion.restype = c_bool
    dll.LogiUpdate.restype = c_bool
    dll.LogiGetState.restype = POINTER(CDIJOYSTATE2)
    dll.LogiGetDevicePath.restype = c_bool
    dll.LogiGetFriendlyProductName.restype = c_bool
    dll.LogiIsConnected.restype = c_bool
    dll.LogiIsDeviceConnected.restype = c_bool
    dll.LogiIsManufacturerConnected.restype = c_bool
    dll.LogiIsModelConnected.restype = c_bool
    dll.LogiButtonTriggered.restype = c_bool
    dll.LogiButtonReleased.restype = c_bool
    dll.LogiButtonIsPressed.restype = c_bool
    dll.LogiGenerateNonLinearValues.restype = c_bool
    dll.LogiGetNonLinearValue.restype = c_int
    dll.LogiHasForceFeedback.restype = c_bool
    dll.LogiIsPlaying.restype = c_bool
    dll.LogiPlaySpringForce.restype = c_bool
    dll.LogiStopSpringForce.restype = c_bool
    dll.LogiPlayConstantForce.restype = c_bool
    dll.LogiStopConstantForce.restype = c_bool
    dll.LogiPlayDamperForce.restype = c_bool
    dll.LogiStopDamperForce.restype = c_bool
    dll.LogiPlaySideCollisionForce.restype = c_bool
    dll.LogiPlayFrontalCollisionForce.restype = c_bool
    dll.LogiPlayDirtRoadEffect.restype = c_bool
    dll.LogiStopDirtRoadEffect.restype = c_bool
    dll.LogiPlayBumpyRoadEffect.restype = c_bool
    dll.LogiStopBumpyRoadEffect.restype = c_bool
    dll.LogiPlaySlipperyRoadEffect.restype = c_bool
    dll.LogiStopSlipperyRoadEffect.restype = c_bool
    dll.LogiPlaySurfaceEffect.restype = c_bool
    dll.LogiStopSurfaceEffect.restype = c_bool
    dll.LogiPlayCarAirborne.restype = c_bool
    dll.LogiStopCarAirborne.restype = c_bool
    dll.LogiPlaySoftstopForce.restype = c_bool
    dll.LogiStopSoftstopForce.restype = c_bool
    dll.LogiSetPreferredControllerProperties.restype = c_bool
    dll.LogiGetCurrentControllerProperties.restype = c_bool
    dll.LogiGetShifterMode.restype = c_int
    dll.LogiSetOperatingRange.restype = c_bool
    dll.LogiGetOperatingRange.restype = c_bool
    dll.LogiPlayLeds.restype = c_bool
    dll.LogiSteeringShutdown.restype = c_void_p


def initialize_with_window(ignore_x_input_controllers: bool, hwnd: int):
    """
    Call this function to initialize if you have already the window handle
    """

    return dll.LogiSteeringInitializeWithWindow(c_bool(ignore_x_input_controllers), c_long(hwnd))


def initialize(ignore_x_input_controllers: bool):
    """
    Call this function before any other of the following
    """

    return dll.LogiSteeringInitialize(c_bool(ignore_x_input_controllers))


def get_sdk_version():
    """
    Get the current SDK Version number
    """
    major_version = c_int64()
    minor_version = c_int64()
    build_version = c_int64()

    result = dll.LogiSteeringGetSdkVersion(
        byref(major_version),
        byref(minor_version),
        byref(build_version)
    )

    return major_version.value, minor_version.value, build_version.value, result


def update():
    """
    Update the status of the controller
    """

    return dll.LogiUpdate()


def get_state(index: int) -> DIJOYSTATE2:
    """
    Get the state of the controller in the standard way.

    :returns DIJOYSTATE2*
    """
    c_struct_state_pointer = dll.LogiGetState(c_int(index))
    return DIJOYSTATE2.from_c_struct(c_struct_state_pointer.contents)


def get_c_state(index: int) -> CDIJOYSTATE2:
    """
    Get the state of the controller in the standard way.

    :returns DIJOYSTATE2*
    """
    c_struct_state_pointer = dll.LogiGetState(c_int(index))
    return c_struct_state_pointer.contents


def get_device_path(index: int, buffer_size: int):
    """
    Get the computer specific operating system assigned controller GUID at a given index
    """

    buffer = create_unicode_buffer(buffer_size)
    result = dll.LogiGetDevicePath(
        c_int(index),
        byref(buffer),
        c_int(buffer_size)
    )

    return buffer.value, result


def get_friendly_product_name(index: int, buffer_size: int):
    """
    Get the friendly name of the product at index
    """

    buffer = create_unicode_buffer(buffer_size)
    result = dll.LogiGetFriendlyProductName(
        c_int(index),
        byref(buffer),
        c_int(buffer_size)
    )

    return buffer.value, result


def is_connected(index: int):
    """
    Check if a generic device at index is connected
    """

    return dll.LogiIsConnected(c_int(index))


def is_device_connected(index: int, device_type: DeviceType):
    """
    Check if the device connected at index is of the same type specified by deviceType
    """

    return dll.LogiIsDeviceConnected(c_int(index), c_int(device_type.value))


def is_manufacturer_connected(index: int, manufacturer: Manufacurer):
    """
    Check if the device connected at index is made from the manufacturer specified by manufacturerName
    """

    return dll.LogiIsManufacturerConnected(c_int(index), c_int(manufacturer.value))


def is_model_connected(index: int, model: Model):
    """
    Check if the device connected at index is the model specified by modelName
    """

    return dll.LogiIsModelConnected(c_int(index), c_int(model.value))


def button_triggered(index: int, button_number: int):
    """
    Check if the device connected at index is currently triggering the button specified by button_number
    """

    return dll.LogiButtonTriggered(c_int(index), c_int(button_number))


def button_released(index: int, button_number: int):
    """
    Check if on the device connected at index has been released the button specified by button_number
    """

    return dll.LogiButtonReleased(c_int(index), c_int(button_number))


def button_is_pressed(index: int, button_number: int):
    """
    Check if on the device connected at index is currently being pressed the button specified by button_number
    """

    return dll.LogiButtonIsPressed(c_int(index), c_int(button_number))


def generate_non_linear_values(index: int, non_linear_coefficient: int):
    """
    Generate non-linear values for the axis of the controller at index
    """

    return dll.LogiGenerateNonLinearValues(c_int(index), c_int(non_linear_coefficient))


def get_non_linear_value(index: int, input_value: int):
    """
    Get a non-linear value from a table previously generated
    """

    return dll.LogiGetNonLinearValue(c_int(index), c_int(input_value))


def has_force_feedback(index: int):
    """
     Check if the controller at index has force feedback
     """

    return dll.LogiHasForceFeedback(c_int(index))


def is_playing(index: int, force_type: ForceType):
    """
    Check if the controller at index is playing the force specified by forceType
    """

    return dll.LogiIsPlaying(c_int(index), c_int(force_type.value))


def play_spring_force(index: int, offset_percentage: int, saturation_percentage: int, coefficient_percentage: int):
    """
    Play the spring force on the controller at index with the specified parameters
    """

    return dll.LogiPlaySpringForce(c_int(index), c_int(offset_percentage),
                                   c_int(saturation_percentage), c_int(coefficient_percentage))


def stop_spring_force(index: int):
    """
    Stop the spring force on the controller at index
    """

    return dll.LogiStopSpringForce(c_int(index))


def play_constant_force(index: int, magnitude_percentage: int):
    """
    Play the constant force on the controller at index with the specified parameter
    """

    return dll.LogiPlayConstantForce(c_int(index), c_int(magnitude_percentage))


def stop_constant_force(index: int):
    """
    Stop the constant force on the controller at index
    """

    return dll.LogiStopConstantForce(c_int(index))


def play_damper_force(index: int, coefficient_percentage: int):
    """
    Play the damper force on the controller at index with the specified parameter
    """

    return dll.LogiPlayDamperForce(c_int(index), c_int(coefficient_percentage))


def stop_damper_force(index: int):
    """
    Stop the damper force on the controller at index
    """

    return dll.LogiStopDamperForce(c_int(index))


def play_side_collision_force(index: int, magnitude_percentage: int):
    """
    Play the side collision force on the controller at index with the specified parameter
    """

    return dll.LogiPlaySideCollisionForce(c_int(index), c_int(magnitude_percentage))


def play_frontal_collision_force(index: int, magnitude_percentage: int):
    """
    Play the frontal collision force on the controller at index with the specified parameter
    """

    return dll.LogiPlayFrontalCollisionForce(c_int(index), c_int(magnitude_percentage))


def play_dirt_road_effect(index: int, magnitude_percentage: int):
    """
    Play the dirt road effect on the controller at index with the specified parameter
    """

    return dll.LogiPlayDirtRoadEffect(c_int(index), c_int(magnitude_percentage))


def stop_dirt_road_effect(index: int):
    """
    Stop the dirt road effect on the controller at index
    """

    return dll.LogiStopDirtRoadEffect(c_int(index))


def play_bumpy_road_effect(index: int, magnitude_percentage: int):
    """
    Play the bumpy road effect on the controller at index with the specified parameter
    """

    return dll.LogiPlayBumpyRoadEffect(c_int(index), c_int(magnitude_percentage))


def stop_bumpy_road_effect(index: int):
    """
    Stop the bumpy road effect on the controller at index
    """

    return dll.LogiStopBumpyRoadEffect(c_int(index))


def play_slippery_road_effect(index: int, magnitude_percentage: int):
    """
    Play the slippery road effect on the controller at index with the specified parameter
    """

    return dll.LogiPlaySlipperyRoadEffect(c_int(index), c_int(magnitude_percentage))


def stop_slippery_road_effect(index: int):
    """
    Stop the slippery road effect on the controller at index
    """

    return dll.LogiStopSlipperyRoadEffect(c_int(index))


def play_surface_effect(index: int, effect_type: int, magnitude_percentage: int,
                        periodic_effect: PeriodicSurfaceEffect):
    """
    Play the surface effect on the controller at index with the specified parameter
    """

    return dll.LogiPlaySurfaceEffect(c_int(index), c_int(effect_type),
                                     c_int(magnitude_percentage), c_int(periodic_effect.value))


def stop_surface_effect(index: int):
    """
    Stop the surface effect on the controller at index
    """

    return dll.LogiStopSurfaceEffect(c_int(index))


def play_car_airborne(index: int):
    """
    Play the car airborne effect on the controller at index
    """

    return dll.LogiPlayCarAirborne(c_int(index))


def stop_car_airborne(index: int):
    """
    Stop the car airborne effect on the controller at index
    """

    return dll.LogiStopCarAirborne(c_int(index))


def play_soft_stop_force(index: int, usable_range_percentage: int):
    """
     Play the soft stop force on the controller at index with the specified parameter
     """

    return dll.LogiPlaySoftstopForce(c_int(index), c_int(usable_range_percentage))


def stop_soft_stop_force(index: int):
    """
    Stop the soft stop force on the controller at index
    """

    return dll.LogiStopSoftstopForce(c_int(index))


def set_preferred_controller_properties(properties: ControllerProperties):
    """
    Set preferred wheel properties specified by the struct properties
    """

    return dll.LogiSetPreferredControllerProperties(properties.as_c_struct())


def get_current_controller_properties(index: int):
    """
    Fills the properties parameter with the current controller properties
    """

    c_type_properties = CControllerProperties()
    data = create_unicode_buffer(36)

    result = dll.LogiGetCurrentControllerProperties(
        c_int(index),
        pointer(c_type_properties)
    )

    if result:
        python_properties = ControllerProperties.from_c_struct(
            c_type_properties)
        return python_properties, result
    else:
        return None, result


def get_shifter_mode(index: int):
    """
    get current shifter mode (gated or sequential)
    """

    return dll.LogiGetShifterMode(c_int(index))


def set_operating_range(index: int, motion_range: int):
    """
    Sets the operating range in degrees on the controller at the index.
    """

    return dll.LogiSetOperatingRange(c_int(index), c_int(motion_range))


def get_operating_range(index: int):
    """
    Gets the current operating range in degrees on the controller at the index.
    """

    motion_range = c_int()
    result = dll.LogiGetOperatingRange(
        c_int(index), byref(motion_range)
    )

    return motion_range.value, result


def play_leds(index: int, current_rpm: float, rpm_first_led_turns_on: float, rpm_red_line: float):
    """
    Play the LEDs on the controller at index applying the specified parameters.
    """

    return dll.LogiPlayLeds(
        c_int(index),
        c_float(current_rpm),
        c_float(rpm_first_led_turns_on),
        c_float(rpm_red_line)
    )


def shutdown():
    """
    Call this function to shutdown the SDK and destroy the controller and wheel objects
    """

    return dll.LogiSteeringShutdown()
