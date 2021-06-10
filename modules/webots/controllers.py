'''
Created by: Craig Fouts
Created on: 6/10/2021
'''


# class ControllerAdapter:

#     def __init__(self, controller):
#         self.controller = controller()
#         methods = {method: getattr(self.controller, method) for method in
#                    dir(self.robot) if not method.startswith('_')}
#         self.__dict__.update(methods)

#     def __getattr__(self, name):
#         return getattr(self.robot, name)


class ControllerAdapter:

    def __init__(self, controller, **attributes):
        self.controller = controller()
        self.__dict__.update(attributes)

    def __getattr__(self, name):
        return getattr(self.controller, name)

    def move_forward(self, distance, speed):
        self.controller.move_forward(distance, speed)

    def move_backward(self, distance, speed):
        self.controller.move_backward(distance, speed)

    def strafe_right(self, distance, speed):
        self.controller.strafe_right(distance, speed)

    def strafe_left(self, distance, speed):
        self.controller.strafe_left(distance, speed)

    def turn_right(self, degrees, speed):
        self.controller.turn_right(degrees, speed)

    def turn_left(self, degrees, speed):
        self.controller.turn_left(degrees, speed)

    def raise_arm(self, distance, speed):
        self.controller.raise_arm(distance, speed)

    def lower_arm(self, distance, speed):
        self.controller.lower_arm(distance, speed)

    def open_fingers(self, distance, speed):
        self.controller.open_fingers(distance, speed)

    def close_fingers(self, distance, speed):
        self.controller.close_fingers(distance, speed)


if __name__ == '__main__':
    controller = ControllerAdapter(TestRobot)
    controller.say('Hello, World')
