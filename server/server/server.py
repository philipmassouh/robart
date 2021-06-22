import os
import subprocess
import socketserver
from server.server.order_manager import OrderManager


class Server(socketserver.BaseRequestHandler):
    def __init__(self, host="192.168.1.31", port=8000):
        # Check if webots is running. Takes a moment.
        started = False
        r = os.popen('tasklist /v').read().strip().split('\n')  # Gets all running exes.
        for i in range(len(r)):                                 # Loops through all exes.
            if "webotsw.exe" in r[i]:
                started = True
                break

        # Opens webots if it wasn't running.
        if not started:
            # Webots location and world.
            webots = os.environ.get('WEBOTS_HOME') + "/msys64/mingw64/bin/webotsw.exe"
            world = os.getcwd() + "/assets/warehouse.wbt"

            # Opens webots.
            subprocess.Popen([webots, "--stream", world])

            # Pauses for program to open for a moment.
            # Using a for loop so its based on the system.
            for q in range(150000000):
                # Little loading bar for fun.
                if (q + 1) % 1500000 == 0:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(' ', int(q / 1500000), '.0%', sep='')
                    for _ in range(int(q / 1500000)):
                        print('=', end='')

            # Clear and newline to look nice.
            os.system('cls' if os.name == 'nt' else 'clear')
            print()

        # Initializes variables.
        self.HOST = host
        self.PORT = port
        self.om = OrderManager()
        self.running = False

    # Makes object callable.
    def __call__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Handles HTTP requests.
    def handle(self):
        self.running = False

    # Manages GET requests.
    def do_GET(self):
        pass

    # Manages PUT requests.
    def do_PUT(self):
        pass

    # Starts the server.
    def start(self):
        # Starts the order manager.
        self.om.start()

        # Starts the server.
        self.running = True

        # Starts the server.
        with socketserver.TCPServer((self.HOST, self.PORT), self) as httpd:
            print("Server started at: ", self.HOST, self.PORT)

            # HTTP request loop.
            while self.running:
                httpd.handle_request()

            # Stops server and order manager.
            httpd.server_close()
            self.om.stop()
