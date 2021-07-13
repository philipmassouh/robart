import threading
import json
import string
from server.controller.controllers import RobotController, WebotsRobot


class OrderManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        # Opens database.
        file = open('./server/server/database.json')

        # Initial variables.
        self.running = True
        self.orders = []
        self.orders_hist = []
        self.database = json.load(file)
        self.controller = RobotController(WebotsRobot, "Robart")

    # Starts the order manager.
    def run(self):
        while self.running:
            if len(self.orders) > 0:
                # Gets the oldest order.
                order = self.orders.pop(0)
                operation = order[0]
                data = order[1]

                # Tests if the op is get or put.
                if operation == 'get':
                    # Gets the number or items requested.
                    for _ in range(data[2]):
                        last = self.database['objects'][data[0]]['count'] - 1

                        if last > -1:
                            # Gets the item requested.
                            coords = self.database['objects'][data[0]]['entities'][last]['pos']
                            self.controller.get_at_coords(coords)

                            # Update count object and free space.
                            self.database['objects'][data[0]]['count'] = last
                            self.database['objects'][data[0]]['entities'].pop(last)
                            self.database['freeSpace'].append(coords)
                            self.database['table'].append(data[0])
                else:
                    for _ in range(data[2]):
                        # Where the item needs to be placed.
                        coords = self.database['freeSpace'].pop(0)
                        data[1]['pos'] = coords
                        name = data[0]
                        data[1]['sku'] = self.int_to_sku(self.database['nextSKU'])

                        if data[0] in ['that', 'this', 'it']:
                            name = self.database['table'].pop(0)

                        # Check if it is there.
                        if self.database['objects'][name].get('count') is None:
                            self.database['objects'][name]['count'] = 0
                            self.database['objects'][name]['description'] = ''
                            self.database['objects'][name]['entities'] = []

                        # Go to place it.
                        self.controller.goto_coords(coords)

                        # Add the item to the database.
                        self.database['objects'][name]['count'] += 1
                        self.database['objects'][name]['entities'].append(data[1])
                        self.database['nextSKU'] += 1

                # Adds order to history.
                self.orders_hist.append(order)

    # Takes the number stored in the database and turns it into a sku.
    def int_to_sku(self, number):
        r = ''
        while number > 0:
            r = string.printable[number % 36] + r
            number //= 36

        if len(r) < 12:
            # Format string.
            a = ''
            for _ in range(12 - len(r)):
                a += '0'

            r = a + r
            return r
        elif len(r) > 12:
            # Starts from 0 again if it overflows.
            self.database['nextSKU'] = 0
            return self.int_to_sku(0)
        else:
            return r

    # Adds an item to order.
    def add_order(self, order):
        self.orders.append(order)

    # Gets all old orders.
    def get_order_hist(self):
        return self.orders_hist

    # Stops the order manager and saves the DB.
    def stop(self):
        # Saves the changes to the database.
        file = open('./server/server/database.json', 'w')
        file.write(json.dumps(self.database, indent=4, sort_keys=True))
        file.close()

        self.running = False
