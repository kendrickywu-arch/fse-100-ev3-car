#!/usr/bin/env pybricks-micropython
#client_control-1.py
import socket
from pynput import keyboard


def control_ev3(ev3_ip, ev3_port):
    '''
    Connects to an EV3 server and controls it using keyboard inputs.
    Args:
        ev3_ip (str): IP address of the EV3 server.
        ev3_port (int): Port number of the EV3 server.
    '''
    #connect to EV3 server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ev3_ip, ev3_port))

    def on_press(key):
        try:
            if key.char in ("w", "a", "s", "d", "f", "g", "c", "p", "l"):
                command = f"{key.char}d".encode() #"d" for key down
                client_socket.send(command)
        except AttributeError:
            pass # ignore other keys
    def on_release(key):
        try:
            if key.char in ("w", "a", "s", "d", "f", "g", "c", "p", "l"):
                command = f"{key.char}u".encode() #"u" for key up
                client_socket.send(command)

        except AttributeError:
            pass


    try:
        #start listening for keyboard events
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    finally:
        #close socket when done
        client_socket.close()

if __name__ == "__main__":
    EV3_IP = "192.168.0.34" #EV3 IP address on top corner of EV3 screen
    EV3_PORT = 12345
    control_ev3(EV3_IP, EV3_PORT)