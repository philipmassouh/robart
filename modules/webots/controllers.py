'''
Created by: Craig Fouts
Created on: 6/10/2021
'''

from abc import ABC, abstractmethod
from webots.controller import Robot


class RobotController:

    def __init__(self, robot):
        self.robot = robot()
        methods = {method: getattr(self.robot, method) for method in
                   dir(self.robot) if not method.startswith('_') and
                   method.endswith('_')}
        self.__dict__.update(methods)

    def __getattr__(self, name):
        return getattr(self.robot, name)


class AbstractController(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def drive_forward_(self, distance, speed): pass

    @abstractmethod
    def drive_backward_(self, distance, speed): pass

    @abstractmethod
    def strafe_right_(self, distance, speed): pass

    @abstractmethod
    def strafe_left_(self, distance, speed): pass

    @abstractmethod
    def turn_right_(self, degrees, speed): pass

    @abstractmethod
    def turn_left_(self, degrees, speed): pass

    @abstractmethod
    def raise_arm_(self, distance, speed): pass

    @abstractmethod
    def lower_arm_(self, distance, speed): pass

    @abstractmethod
    def open_fingers_(self): pass

    @abstractmethod
    def close_fingers_(self): pass


class TextRobot(AbstractController):

    def __init__(self):
        super().__init__()

    def drive_forward_(self, distance, speed):
        output = f'Driving forward distance {distance} at speed {speed}'
        print(output)
        return output

    def drive_backward_(self, distance, speed):
        output = f'Driving backward distance {distance} at speed {speed}'
        print(output)
        return output

    def strafe_right_(self, distance, speed):
        output = f'Strafing right distance {distance} at speed {speed}'
        print(output)
        return output

    def strafe_left_(self, distance, speed):
        output = f'Strafing left distance {distance} at speed {speed}'
        print(output)
        return output

    def turn_right_(self, degrees, speed):
        output = f'Turning right {degrees} degrees at speed {speed}'
        print(output)
        return output

    def turn_left_(self, degrees, speed):
        output = f'Turning left {degrees} degrees at speed {speed}'
        print(output)
        return output

    def raise_arm_(self, distance, speed):
        output = f'Raising arm distance {distance} at speed {speed}'
        print(output)
        return output

    def lower_arm_(self, distance, speed):
        output = f'Lowering arm distance {distance} at speed {speed}'
        print(output)
        return output

    def open_fingers_(self):
        output = 'Opening fingers'
        print(output)
        return output

    def close_fingers_(self):
        output = 'Closing fingers'
        print(output)
        return output


if __name__ == '__main__':
    controller = RobotController(TextRobot)
    controller.drive_forward_(100, 10)
