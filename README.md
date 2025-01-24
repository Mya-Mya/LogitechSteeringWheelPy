# LogitechSteeringWheelPy

This module allows access from Python to the steering wheel SDK provided by Logitech for their gaming steering wheels. The API of this module is the same as the "Logitech Gaming Steering Wheel SDK" version 8.75.30. This SDK and it's documentation can be downloaded from the [Logitech G website](https://www.logitechg.com/en-us/innovation/developer-lab.html). The module has been tested on Python 3.12 and only works on Windows.  

This module includes part of the before mentioned steering wheel SDK (the `LogitechSteeringwheel.dll` and `LogitechSteeringWheelEnginesWrapper.dll` files). These files do not fall under the open source license with the rest of the module. They are re-distributed with permission from Logitech (also see the README file in the SDK). Therefore, there is no need to obtain the SDK. The only dependency of this module is the Logitech Gaming Software.

# Installation

This module requires the `LogitechSteeringWheelEnginesWrapper.dll` file in "Logitech Gaming Steering Wheel SDK".
The file can be downloaded from the [Logitech G website](https://www.logitechg.com/en-us/innovation/developer-lab.html).
After downloading, save the DLL file to somewhere you like.
Please do not forget the path of the DLL file.

# Steps to Use

This section describes how to establish communication with your steering wheel device and read the states of the device.

### 1. Connect your device with your PC.
### 2. Launch GUI window.
To communicate with the device, **we need to have GUI window** and **must to know the id of the window** (`HWND` variable in C/C++ programming).
In addition, note that functions work **only when the GUI window is active**.
These conditions are required by the Logitech Gaming Steering Wheel SDK.

**Example**: Pygame can launch window and we can get the id of the window:
```python
import pygame
pygame.init()
screen = pygame.display.set_mode((640, 200))
hwnd = pygame.display.get_wm_info()["window"] # The ID of the Window !
```
### 3. Load the DLL file of the SDK.
This module is just a wrapper of the Logitech Gaming Steering Wheel SDK.
To use any function of the SDK, we have to load the core file of the SDK, i.e. the `LogitechSteeringWheelEnginesWrapper.dll`, at first.
```python
import LogitechSteeringWheelPy as lsw
lsw.load_dll("Path to the DLL File")
```

### 4. Initialize the SDK.
From here, we start to use the SDK functions.
First, we need to call `initialize_with_window` (`LogiSteeringInitializeWithWindow` in C/C++) to establish the communication between your PC and the device.
```python
initialized = lsw.initialize_with_window(True, hwnd)
assert initialized
```
To proceed, the return value should be `True`, or you cannot get any data from the SDK.

### 5. Have Fun !
The `LogitechSteeringWheelPy/gateway.py` provides a wrapper functions of the Logitech Gaming Steering Wheel SDK.
For more detail on each function, please refer to the documentation of the SDK.

### 6. DON'T FORGET - AT THE END OF YOUR PROGRAM
**Do not forget to call `shutdown` at the end of your program**.
If you forget, the Python process will not exit unless you use the Task Manager !!
```python
lsw.shutdown()
```

# For G29 Users

We have prepared a simple higher-level API for G29 device.
If you are using G29, the `G29` class is useful.

### How to Use

After performing 1, 2, 3, and 4 shown in the Steps to Use section, launch the `G29` instance.
```python
g29 = lsw.G29(
    index=0, # Device number
    positive_angle="counterclockwise" # Positive direction of steering wheel angle
)
```

Call the `update` function of the `G29` instance and the `update` function of the wrapper functions of the SDK on each frame of your game.
This function internally calls `get_state` function to parse the state data of the G29 device, into a usable format.
```pyton
lsw.update()
g29.update()
```
And do not forget to shutdown at the end of your program.
```python
lsw.shutdown()
```

### Available Values

The following values are available in the `G29` class.

Name | Unit/Range/Type | Description
--- | --- | ---
`steering_range_rad` | rad | The oprating range of the steering. This value can be changed in the [G-Hub](https://www.logitechg.com/en-us/innovation/g-hub.html) app.
`steering_rad` | rad | The steering angle.
`throttle_normalized` | $[0,1]$ | 0 when not stepped on the throttle, 1 when stepped on the throttle.
`brake_normalized` | $[0,1]$ | 0 when not stepped on the brake, 1 when stepped on the brake.
`updated_at` | `datetime` | The datetime the state data was retrieved from the G29 device.

**Example**: When you want to print the steering range...
```python
print(g29.steering_range_rad)
```

### Future Works

We would like to be able to provide the following values.

* POV buttons triggered/released checking