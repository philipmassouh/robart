'''
Created by: Craig Fouts, Noah LaPolt, Philip Massouh, Dennis Sweeney
Created on: 5/22/2021
'''
from server.server.server import Server
import sys

if __name__ == '__main__':
    if len(sys.argv) > 2:
        server = Server(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        server = Server(sys.argv[1])
    else:
        server = Server()

    server.start()
