#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait

# Initialize the EV3 brick and color sensor
ev3 = EV3Brick()
color_sensor = ColorSensor (Port.S4) # Adjust port if needed

# Define a dictionary for color-to-frequency mapping
color_beep_frequencies = {
    Color.BLACK: 200,   # Black -> 200 Hz
    Color.BLUE: 400,    # Blue -> 400 Hz
    Color.GREEN: 600,   # Green -> 600 Hz
    Color.YELLOW: 800, # Yellow -> 800 Hz
    Color.RED: 1000,    # Red -> 1000 Hz
    Color.WHITE: 1200,  # White -> 1200 Hz
    Color.BROWN: 1400   # Brown -> 1400 Hz
}

try:
    while True:
        # Get the detected color
        color = color_sensor.color()

        # Check if the detected color has a corresponding beep frequency
        if color in color_beep_frequencies:
            # Play the beep with the corresponding frequency
            ev3.speaker.beep(frequency=color_beep_frequencies [color], duration=50)
        else:
            # Beep with a default frequency for unknown colors
            ev3.speaker.beep(frequency=100, duration=50)

        # Wait briefly before the next reading

except KeyboardInterrupt:
# Graceful exit when user interrupts the program
# ev3.speaker.beep(frequency=500, duration=50)