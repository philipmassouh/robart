import os
import json
import subprocess
import socketserver
# from ibm_watson import DiscoveryV2
from server.server.order_manager import OrderManager
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class Server(socketserver.BaseRequestHandler):
    # Server constructor.
    def __init__(self, host="192.168.1.31", port=8000):
        # Opens webots.
        self.webots_search()

        # Initializes variables.
        self.HOST = host
        self.PORT = port
        self.om = OrderManager()
        self.running = False

        # Open Authentication JSON
        f = open('restAuth.json')
        self.auth = json.load(f)
        f.close()

    # Makes object callable.
    def __call__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Attempts to turn on server webots.
    def webots_search(self):
        started = False
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
            world = os.getcwd() + "./assets/worlds/warehouse.wbt"

            # Opens webots.
            subprocess.Popen([webots, "--stream", world])

            # Pauses for program to open for a moment.
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

    # Handles HTTP requests.
    def handle(self):
        try:
            # Gets and seperates client request.
            data = str(self.request.recv(1024), "utf-8").split('\n')
            header_end = data.index('\r')
            method = data[0]

            # Handles the different HTTP requests.
            if 'PUT' in method:
                message = data[header_end + 1:len(data)]

                # Gets the message as json.
                json_dict = json.loads(message[0])

                # Creates the command.
                self.generate_command(json_dict)
            else:
                # Crashes if it gets a response it doesn't like.
                self.response('503 Service Unavailable', 'This server is not normal.')
                self.stop()
        except UnicodeDecodeError:
            # Crashes if it gets a response it doesn't like.
            self.response('503 Service Unavailable', 'This server is not normal.')
            self.stop()

    # Gets intent, descriptors, location and the object.
    def generate_command(self, message):
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
                if entity_con > 0.50 or o_index == -1:
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

        # Checks for errors.
        self.error_check(wa_intent, wa_entities, o_index)

    # Checks for errors.
    def error_check(self, wa_intent, wa_entities, o_index):
        if len(wa_entities) == 0:
            # Inform client that there is no object.
            self.response('409 Conflict', 'No object found.')
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
                # Sees if the object to be got is on the database.
                if wa_intent[0] == "get":
                    to_get = self.check_database(wa_entities, o_index)

                    if len(to_get) == 1:
                        # Adds the get order to the order stack.
                        self.om.add_order(('get', to_get[0]))

                        # Inform the client that all is well then get the item.
                        res = "I am getting a " + wa_entities[o_index][1] + "."
                        self.response("200 OK", res)
                    else:
                        # Send alternatives.
                        res = 'Could not determine object.\r\n' + '\r\n'.join(to_get)
                        self.response("409 Conflict", res)
                else:
                    # Sends put order.
                    self.om.add_order((
                        'put',
                        (wa_entities[o_index][1], {'pos': [0.0, 0.0], 'sku': '000000000000'}, 1)
                    ))

                    # Inform the client that all is well then put the item.
                    res = "I am placing " + wa_entities[o_index][1] + " away."
                    self.response("200 OK", res)

                # Log data in console.
                print("Recivied data from -", self.client_address, "Command generic:",
                      wa_intent[0], "-", wa_entities[o_index][1])
            else:
                # Inform client that there is no object.
                self.response('409 Conflict', 'No object found.')

    # Returns the database row or rows of the item or items that are requested.
    def check_database(self, entites, index):
        name = entites[index][1]
        exact = self.om.database['objects'].get(name)

        print(exact)

        if exact is not None:
            return [(name, exact, 1)]
        else:
            # Authenticate discovery.
            # auth = self.auth['discovery']
            # authenticator = IAMAuthenticator(auth['apikey'])
            # discovery = DiscoveryV2(
            #     version='2019-11-22',
            #     authenticator=authenticator
            # )

            # discovery.set_service_url(auth['serviceUrl'])

            # Go to discovery and find related words.

            # Return names of related objects.
            return ['Apple', 'Bottle', 'Can', 'Extinguisher', 'Gnome', 'Orange', 'Paint', 'Water']

    # Sends the client a HTTP response.
    def response(self, code, message='All good.'):
        self.request.send(bytes("HTTP/1.1 " + code + '\r\n\n' + message + '\r\n', 'utf-8'))

    # Stops the server.
    def stop(self):
        self.running = False

    # Starts the server.
    def start(self):
        # Starts the order manager and lets server run.
        self.om.start()
        self.running = True

        # Starts the server.
        with socketserver.TCPServer((self.HOST, self.PORT), self) as httpd:
            # Prints confirmation that it runs.
            print("Server started at: ", self.HOST, self.PORT)

            # HTTP request loop.
            while self.running:
                httpd.handle_request()

            # Stops server and order manager.
            httpd.server_close()
            self.om.stop()
