import os
import json
import subprocess
import socketserver
from server.server.order_manager import OrderManager

class Server(socketserver.BaseRequestHandler):
    def __init__(self, host="192.168.1.31", port=8000):
        started = True
        # Check if webots is running. Takes a moment.
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
        #self.om = OrderManager()
        self.running = False

    # Makes object callable.
    def __call__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    # Handles HTTP requests.
    def handle(self):
        data = str(self.request.recv(1024), "utf-8").split('\n')
        header_end = data.index('\r')
        method = data[0]
        header = data[1:header_end]

        # Handles the different HTTP requests.
        if 'PUT' in method:
            message = data[header_end + 1:len(data)]

            # Gets the message as json.
            json_dict = json.loads(message[0])

            # Creates the command.
            self.generate_command(header, json_dict)
        else:
            self.response('503 Service Unavailable', 'This server is not normal.')
            self.stop()

    # Gets intent, descriptors, location and the object.
    def generate_command(self, header, message):
        # Log data in console.
        print("Recivied data from -", self.client_address)

        # List of intents and list of entites.
        intents = message['output']['intents']
        entites = message['output']['entities']

        # Sorts the most likly intent.
        wa_intent = ('get', 0)
        for intent in intents:
            if intent['confidence'] > wa_intent[1]:
                wa_intent = (intent['intent'], intent['confidence'])

        # Sorts out all entities.
        wa_entities = []
        for entity in entites:
            # Entity values.
            entity_nam = entity['entity']
            entity_val = entity['value']
            entity_con = entity['confidence']

            # Indexes
            index = -1
            o_index = -1
            l_index = -1

            # Checks if the entity exists already in the list.
            for i, wa_entity in enumerate(wa_entities):
                # Finds object and location in the current entities.
                if wa_entity[0] == 'object' or wa_entity[0] == 'SKU':
                    o_index = i
                elif wa_entity[0] == 'location':
                    l_index = i
                
                # Finds current value in all entities.
                if entity_val == wa_entity[1]:
                    index = i

            # Creats an List of tuples that hold the command.
            if index == -1:
                if entity_con > 0.50:
                    # Ensures one object and one location.
                    if (entity_nam == 'object' or entity_nam == 'SKU') and o_index != -1:
                        if entity_con > wa_entities[o_index][2]:
                            wa_entities[o_index] = (entity_nam, entity_val, entity_con)
                    elif entity_nam == 'location' and l_index != -1:
                        if entity_con > wa_entities[l_index][2]:
                            wa_entities[l_index] = (entity_nam, entity_val, entity_con)
                    else:
                        wa_entities.append((entity_nam, entity_val, entity_con))
            else:
                if entity_con > wa_entities[i][2]:
                    wa_entities[i] = (entity_nam, entity_val, entity_con)

        # Error checks.
        if len(wa_entities) == 0:
            # Inform client that there is no object.
            self.response('409 Conflict', 'Could not determind object.')
        else:
            # If there is an object or not.
            found = False
            # Checks if there is at least an object in the list.
            for wa_entity in wa_entities:
                if wa_entity[0] == 'object' or wa_entity[0] == 'SKU':
                    found = True
                    break
            
            # Ensures there is an object.
            if found:
                # Inform the client that all is well.
                self.response("200 OK")
            else:
                # Inform client that there is no object.
                self.response('409 Conflict', 'Could not determind object.')

        # TODO: Add a count to the posible inputs.
        # Check against controller database. Use watson discovery.
        # Ask for more specification if more then one item fits criteria.
        # Which one? : list of items. [send all, display first couple, let user interact.]
        # What kind? : list of types. [send all, display first couple, let user interact.]
        # or inform them that the item was not found.
        # Ensure the number asked for can be got.

        # Kills the server if a kill command was sent.
        # DEV ONLY REMOVE IN PRODUCTION.
        print(wa_intent, wa_entities)
        return (wa_intent, wa_entities)

    # Sends the client a HTTP response.
    def response(self, code, message='All good.'):
        self.request.send(bytes("HTTP/1.1 " + code + '\r\n\n' + message + '\r\n', 'utf-8'))

    def stop(self):
        self.running = False

        # When stoping server restart sim:
        # from controller import Supervisor
        # sup = Supervisor(Robot)
        # sup.simulationReset()

    # Starts the server.
    def start(self):
        # Starts the order manager.
        #self.om.start()

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
            #self.om.stop()
