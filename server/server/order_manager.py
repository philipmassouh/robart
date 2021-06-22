import threading
from server.controller.controllers import RobotController, WebotsController

class OrderManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.orders = []
        self.controller = RobotController(WebotsController, "Robart")
    
    def run(self):
        while self.running:
            # Gets the oldest order.
            if len(self.orders) > 0:
                data = self.orders.pop(0)

                # Move robot to that item.
                print(data)

                # Add to history.

    def add_order(self, order):
        self.orders.append(order)

    def stop(self):
        self.running = False
