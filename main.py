#!/usr/bin/env pybricks-micropython
#main.py
import socket
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor, Motor
from pybricks.tools import wait

#Initialize EV3 components
ev3 = EV3Brick()
left_motor = Motor(Port.D)
right_motor = Motor(Port.A)
weapon = Motor(Port.B)
robot = DriveBase(left_motor, right_motor, wheel_diameter = 55.5, axle_track = 104)
touch_sensor = TouchSensor(Port.S4)
color_sensor = ColorSensor(Port.S1)
color_sensing_mode = False
auto_mode = False

#Server configuration
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))
server_socket.listen(1)
print("Waiting for connection...")
client_socket, address = server_socket.accept()
client_socket.settimeout(0.1)
print("Connected to {}".format(address))

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
        if touch_sensor.pressed():
            ev3.speaker.beep(2000)
            break

        if color_sensing_mode:
            color = color_sensor.color()

            #if color in color_beep_frequencies:
                #ev3.speaker.beep(color_beep_frequencies[color], duration=50)
            if color == Color.RED:
                robot.stop()
                wait(1000)
                #if auto_mode:
                #    robot.drive(50)
            elif color == Color.BLUE:
                robot.stop()
                ev3.speaker.beep(670, 50)
                wait(500)
                ev3.speaker.beep(670, 50)
                #if auto_mode:
                #    robot.drive(50)
            elif color == Color.GREEN:
                robot.stop()
                ev3.speaker.beep(890, 50)
                wait(500)
                ev3.speaker.beep(890, 50)
                wait(500)
                ev3.speaker.beep(890, 50)
                #if auto_mode:
                #    robot.drive(50)
            #else:
                #ev3.speaker.beep(100, duration=50) # Default beep for unknown colors
        
        try:
            command = client_socket.recv(2).decode()
        except OSError:
            # A socket timeout lets the loop check the touch sensor again.
            continue

        if not command:
            break
        if len(command) != 2:
            continue

        key, action = command[0], command[1]
        if auto_mode:
            robot.drive(50, 0)
            

        if action == "d": #Key press
            if key == "w":
                robot.drive(200, 0) #Move forward
            elif key == "s":
                robot.drive(-200, 0) #Move backward
            elif key == "a":
                robot.drive(0, -100) #Turn left
            elif key == "d":
                robot.drive(0, 100) #Turn right
            elif key == "f":
                #ev3.speaker.beep(500) #Make a beep noise
                weapon.run(100)
            elif key == "g":
                #ev3.speaker.beep(1000) #Make a beep noise
                weapon.run(-100)
            elif key == "c":
                color_sensing_mode = not color_sensing_mode
            elif key == "p":
                auto_mode = not auto_mode
                robot.stop()

        elif action == "u": #Key release
            if key in ("w", "a", "s", "d"):
                robot.stop() # Stop the robot on key release
            elif key in ("f", "g"):
                weapon.stop() # Stop the weapon motor on key release
            #elif key == "c":
                #color_sensing_mode = False
            #elif key == "p":
            #    auto_mode = False
            

finally:
    robot.stop()
    client_socket.close()
    server_socket.close()
