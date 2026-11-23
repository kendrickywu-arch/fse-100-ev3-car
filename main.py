#!/usr/bin/env pybricks-micropython
#main.py
import socket
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor, UltrasonicSensor, Motor, GyroSensor
from pybricks.tools import wait

#initialize EV3 components
ev3 = EV3Brick()
left_motor = Motor(Port.D)
right_motor = Motor(Port.A)
weapon = Motor(Port.B)
robot = DriveBase(left_motor, right_motor, wheel_diameter = 55, axle_track = 175)
touch_sensor = TouchSensor(Port.S3)
color_sensor = ColorSensor(Port.S1)
distance_sensor = UltrasonicSensor(Port.S2)
gyro_sensor = GyroSensor(Port.S4)
color_sensing_mode = False
auto_mode = False
touch_handled = False
last_auto_color = None

#server configuration
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))
server_socket.listen(1)
print("Waiting for connection...")
client_socket, address = server_socket.accept()
client_socket.settimeout(0.1)
print("Connected to {}".format(address))

color_beep_frequencies = {
    Color.BLUE: 400,    #blue = 400 Hz
    Color.GREEN: 600,   #green = 600 Hz
    Color.RED: 1000,    #red = 1000 Hz
    Color.YELLOW: 700
    #Color.DARK_BLUE: 300
}

try:
    while True:

        if auto_mode:
            color = color_sensor.color()
            if touch_sensor.pressed():
                if not touch_handled:
                    robot.stop()
                    if distance_sensor.distance() >= 450:
                        #robot.turn(-100)
                        #robot.drive(0,-100)
                        gyro_sensor.reset_angle(0)
                        wait(100)
                        robot.drive(100, 0)
                        wait(1000)
                        while gyro_sensor.angle() > -70:
                            robot.drive(0,-50)# -(50/(gyro_sensor.angle() + 1)))
                            #wait(10)
                        #gyro_sensor.reset_angle(0)
                        robot.drive(100, 0)
                        wait(3000)
                    else:
                        #robot.turn(100)
                        #robot.drive(0,100)
                        gyro_sensor.reset_angle(0)
                        wait(100)
                        robot.drive(100, 0)
                        wait(1000)
                        while gyro_sensor.angle() < 110:
                            robot.drive(0,50)# + (50/(gyro_sensor.angle() + 1)))
                            #wait(10)
                        #gyro_sensor.reset_angle(0)

                    robot.stop()
                    #wait(200)
                    touch_handled = True
            else:
                touch_handled = False

            if color in color_beep_frequencies and color != last_auto_color:
                robot.stop()
                if color == Color.RED:
                    wait(1000)
                elif color == Color.BLUE:
                    ev3.speaker.beep(670, 50)
                    wait(500)
                    ev3.speaker.beep(670, 50)
                elif color == Color.GREEN:
                    ev3.speaker.beep(890, 50)
                    wait(500)
                    ev3.speaker.beep(890, 50)
                    wait(500)
                    ev3.speaker.beep(890, 50)
                last_auto_color = color
            elif color not in color_beep_frequencies:
                last_auto_color = None
            
            if distance_sensor.distance() > 450:
                wait(3000)
                gyro_sensor.reset_angle(0)
                while gyro_sensor.angle() > -70:
                    robot.drive(0, -50)# - (50/(gyro_sensor.angle() + 1)))
                    #wait(10)
                #gyro_sensor.reset_angle(0)
                robot.drive(-100, 0)
                wait(3000)

            robot.drive(-100, 0)
            

        try:
            command = client_socket.recv(2).decode()
        except OSError:
            #socket timeout lets the loop check the touch sensor again
            continue

        if not command:
            break
        if len(command) != 2:
            continue

        key, action = command[0], command[1]
        if action == "d": #key press
            if key == "w":
                robot.drive(-100, 0) #move forward
            elif key == "s":
                robot.drive(100, 0) #move backward
            elif key == "a":
                robot.drive(0, -50) #turn left
            elif key == "d":
                robot.drive(0, 50) #turn right
            elif key == "f":
                weapon.run(100) #forklift up
            elif key == "g":
                weapon.run(-100) #forklift down
            elif key == "c":
                color_sensing_mode = not color_sensing_mode
            elif key == "p":
                gyro_sensor.reset_angle(0)
                auto_mode = not auto_mode
                robot.stop()
            #elif key == "l":
            #    for i in range(distance_sensor.distance()/100):
            #        ev3.speaker.beep(999)
            #    robot.drive(0,100)
                #robot.turn(90)
            #    wait(1720)
            #    robot.stop()

        elif action == "u": #key release
            if key in ("w", "a", "s", "d"):
                robot.stop() # stop the wheel motors on key release
            elif key in ("f", "g"):
                weapon.stop() #stop the forklift motor on key release
            #elif key == "c":
                #color_sensing_mode = False
            #elif key == "p":
            #    auto_mode = False
            

finally:
    robot.stop()
    client_socket.close()
    server_socket.close()
