import threading
from server.controller.controllers import RobotController, WebotsController


class OrderManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.orders = []
        self.orders_hist = []
        self.database = {
            'cube': [[], [(0.0, 0.0), (0.0, 1.0)], 2, ['KIJUEBVUA872', 'Y34IGTYWF13I']]
        }
        self.controller = RobotController(WebotsController, "Robart")

    def run(self):
        while self.running:
            # Gets the oldest order.
            if len(self.orders) > 0:
                order = self.orders.pop(0)
                operation = order[0]
                data = order[1]

                print(order)
                print(data)

                # Tests if the op is get or put.
                if operation == 'get':
                    for _ in range(data[2]):
                        # Remove item from row.
                        coords = data[1][1].pop(len(data[1][1]) - 1)
                        data[1][2] = data[1][2] - 1
                        sku = data[1][3].pop(len(data[1][3]) - 1)

                        # Gets the item requested.
                        #self.controller.goto_coords(coords[0], coords[1])

                        # Updates the database.
                        self.database[data[0]] = data[1]
                else:
                    for _ in range(data[2]):
                        # Put the item back where they go.
                        coords = data[1][1][len(data[1][1]) - 1]
                        #self.controller.goto_coords(coords[0], coords[1])


                        # Add the item to the database.
                        self.database[data[0]][1].append(data[1][1])
                        self.database[data[0]][1] += data[1][2]
                        self.database[data[0]][1].append(data[1][3])

                # Adds order to history.
                self.orders_hist.append(order)

    def add_order(self, order):
        self.orders.append(order)

    def get_order_hist(self):
        return self.orders_hist

    def stop(self):
        self.running = False
