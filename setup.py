from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

name = "LogitechSteeringWheelPy"
setup(
    name=name,
    version='0.0.1',
    packages=['logitech_steering_wheel'],
    license='MIT License',
    description='A wrapper to use the Logitech Steering Wheel SDK in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mya-Mya/LogitechSteeringWheelPy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
