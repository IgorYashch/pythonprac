"""Entrypoint for the client"""

import sys
import socket

from .ClientCmd import MUD_mainloop


PORT = 1337
HOST = "127.0.0.1"


def main():
    """Start fuction for client"""
    if len(sys.argv) != 2:
        print("Enter your user name")
    else:
        username = sys.argv[1]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            s.sendall((username + "\n").encode())
            message = s.recv(1024).decode()

            print(message)

            if message == "Connection created!":
                cmd = MUD_mainloop(s)
                cmd.cmdloop()
            else:
                return


main()
