import http.server
import socketserver
from server.controller.controllers import RobotController, WebotsController

controller = RobotController(WebotsController, "Robart")

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip().decode("utf-8")

        # Manages post methods.
        if 'POST' in self.data:
            pos1 = self.data.find('\"intent\":') + 10
            pos2 = self.data.find('\"value\":') + 9
            intent = self.data[pos1:self.data.find('\"', pos1)]
            value = self.data[pos2:self.data.find('\"', pos2)]

            print(intent, value)

            if value == "cube":
                controller.get_object_('obj1')
            elif value == "box":
                controller.get_object_('obj2')
            elif value == "crate":
                controller.get_object_('obj3')
        
        # Send it worked to the client.
        self.request.sendall(b'HTTP/1.1 200 Success')

class Server:
    def __init__(self, host="192.168.1.31", port=8000):
        self.HOST, self.PORT = host, port

    def start(self):
        with socketserver.TCPServer((self.HOST, self.PORT), Handler) as httpd:
            print("Server started at: ", self.HOST, self.PORT)
            httpd.serve_forever()