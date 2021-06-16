import http.server
import socketserver
from server.controller.controller import Controller

class Handler(socketserver.BaseRequestHandler):
    controller = Controller()

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


        # Send it worked to the client.
        self.request.sendall(b'HTTP/1.1 200 Success')


HOST, PORT = "localhost", 8000

with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()