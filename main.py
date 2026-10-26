#!/usr/bin/env pybricks-micropython
#main.py
import socket
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor, Motor

#Initialize EV3 components
ev3 = EV3Brick()
left_motor = Motor(Port.D)
right_motor = Motor(Port.A)
weapon = Motor(Port.B)
robot = DriveBase(left_motor, right_motor, wheel_diameter = 55.5, axle_track = 104)
touch_sensor = TouchSensor(Port.S4)
color_sensor = ColorSensor(Port.S1)

#Server configuration
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))
server_socket.listen(1)
print("Waiting for connection...")
client_socket, address = server_socket.accept()
client_socket.settimeout(0.1)
print("Connected to {}".format(address))

try:
    while True:
        if touch_sensor.pressed():
            ev3.speaker.beep(2000)
            break

        #if 
        
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
        if action == "d": #Key press
            if key == "w":
                robot.drive(900, 0) #Move forward
            elif key == "s":
                robot.drive(-900, 0) #Move backward
            elif key == "a":
                robot.drive(0, -450) #Turn left
            elif key == "d":
                robot.drive(0, 450) #Turn right
            elif key == "f":
                #ev3.speaker.beep(500) #Make a beep noise
                weapon.run(100)
            elif key == "g":
                #ev3.speaker.beep(1000) #Make a beep noise
                weapon.run(-100)
        elif action == "u": #Key release
            if key in ("w", "a", "s", "d"):
                robot.stop() # Stop the robot on key release
            elif key in ("f", "g"):
                weapon.stop() # Stop the weapon motor on key release

finally:
    robot.stop()
    client_socket.close()
    server_socket.close()