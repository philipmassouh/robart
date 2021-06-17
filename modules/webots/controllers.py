from abc import ABC, abstractmethod
from webots.controller import Robot


TIME_STEP = 32
WMAX_VEL = 14.81
AMAX_VEL = 1.5708


class RobotController:

    def __init__(self, robot, name=None):
        self.robot = robot(name=name) if name else robot()
        methods = {method: getattr(self.robot, method) for method in
                   dir(self.robot) if not method.startswith('_') and
                   method.endswith('_')}
        self.__dict__.update(methods)
        self.object_distances = {
            'obj1': 120,
            'obj2': 240,
            'obj3': 355
        }

    def __getattr__(self, name):
        return getattr(self.robot, name)

    def get_object_(self, object):
        self.robot.drive_forward_(self.object_distances[object], 0.8)
        self.robot.raise_arm_(20, 0.8)
        self.robot.turn_arm_(-30, 0.8)
        self.robot.grab_object_()
        self.robot.turn_arm_(-30, -0.8)
        self.robot.lower_arm_(20, 0.8)
        self.robot.drive_backward_(self.object_distances[object], 0.8)


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

    def __init__(self, name='TextBot'):
        super().__init__()

        self.name = name

    def drive_forward_(self, distance, speed):
        output = f'{self.name}: Driving forward distance {distance} at speed {speed}'
        print(output)
        return output

    def drive_backward_(self, distance, speed):
        output = f'{self.name}: Driving backward distance {distance} at speed {speed}'
        print(output)
        return output

    def strafe_right_(self, distance, speed):
        output = f'{self.name}: Strafing right distance {distance} at speed {speed}'
        print(output)
        return output

    def strafe_left_(self, distance, speed):
        output = f'{self.name}: Strafing left distance {distance} at speed {speed}'
        print(output)
        return output

    def turn_right_(self, degrees, speed):
        output = f'{self.name}: Turning right {degrees} degrees at speed {speed}'
        print(output)
        return output

    def turn_left_(self, degrees, speed):
        output = f'{self.name}: Turning left {degrees} degrees at speed {speed}'
        print(output)
        return output

    def raise_arm_(self, distance, speed):
        output = f'{self.name}: Raising arm distance {distance} at speed {speed}'
        print(output)
        return output

    def lower_arm_(self, distance, speed):
        output = f'{self.name}: Lowering arm distance {distance} at speed {speed}'
        print(output)
        return output

    def open_fingers_(self):
        output = f'{self.name}: Opening fingers'
        print(output)
        return output

    def close_fingers_(self):
        output = f'{self.name}: Closing fingers'
        print(output)
        return output


class WebotsController(AbstractController, Robot):

    def __init__(self, name):
        super().__init__()

        self.name = name
        self.timestep = int(self.getBasicTimeStep())
        self.wheels = [
            self.getDevice('wheel1'),
            self.getDevice('wheel2'),
            self.getDevice('wheel3'),
            self.getDevice('wheel4')
        ]
        self.arms = [
            self.getDevice('arm1'),
            self.getDevice('arm2'),
            self.getDevice('arm3'),
            self.getDevice('arm4'),
            self.getDevice('arm5')
        ]
        self.fingers = [
            self.getDevice('finger1'),
            self.getDevice('finger2')
        ]
        self._initialize()
        self.lower_arm_(40, 0.8)

    def _initialize(self):
        for arm in self.arms:
            arm.setPosition(float('inf'))

        for finger in self.fingers:
            finger.setPosition(float('inf'))

        for wheel in self.wheels:
            wheel.setPosition(float('inf'))

        self._stop_wheels()
        self._stop_arms()
        self._stop_fingers()

    def _wait_for_time(self, time):
        step = 0
        while self.step(self.timestep) != -1 and step < time:
            step += 1

    def _start_driving(self, speed):
        for wheel in self.wheels:
            wheel.setVelocity(speed * WMAX_VEL)

    def _start_strafing(self, speed):
        self.wheels[0].setVelocity(speed * -WMAX_VEL)
        self.wheels[1].setVelocity(speed * WMAX_VEL)
        self.wheels[2].setVelocity(speed * WMAX_VEL)
        self.wheels[3].setVelocity(speed * -WMAX_VEL)

    def _start_turning(self, speed):
        self.wheels[0].setVelocity(speed * WMAX_VEL)
        self.wheels[1].setVelocity(speed * -WMAX_VEL)
        self.wheels[2].setVelocity(speed * WMAX_VEL)
        self.wheels[3].setVelocity(speed * -WMAX_VEL)

    def _stop_wheels(self):
        for wheel in self.wheels:
            wheel.setVelocity(0)

    def _start_arms(self, arms, speeds):
        for arm, speed in zip(arms, speeds):
            self.arms[arm].setVelocity(speed * AMAX_VEL)

    def _stop_arms(self):
        for arm in self.arms:
            arm.setVelocity(0)

    def _start_fingers(self, speed):
        for finger in self.fingers:
            finger.setVelocity(speed)

    def _stop_fingers(self):
        for finger in self.fingers:
            finger.setVelocity(0)

    def drive_forward_(self, distance, speed):
        self._start_driving(speed)
        self._wait_for_time(distance / speed)
        self._stop_wheels()

    def drive_backward_(self, distance, speed):
        self._start_driving(-speed)
        self._wait_for_time(distance / speed)
        self._stop_wheels()

    def strafe_right_(self, distance, speed):
        self._start_strafing(speed)
        self._wait_for_time(distance / speed)
        self._stop_wheels()

    def strafe_left_(self, distance, speed):
        self._start_strafing(-speed)
        self._wait_for_time(distance / speed)
        self._stop_wheels()

    def turn_right_(self, degrees, speed):
        self._start_turning(speed)
        self._wait_for_time(degrees / speed)
        self._stop_wheels()

    def turn_left_(self, degrees, speed):
        self._start_turning(-speed)
        self._wait_for_time(degrees / speed)
        self._stop_wheels()

    def raise_arm_(self, distance, speed):
        self._start_arms([1, 2, 3], [-speed, speed, -speed])
        self._wait_for_time(distance / speed)
        self._stop_arms()

    def lower_arm_(self, distance, speed):
        self._start_arms([1, 2, 3], [speed, -speed, speed])
        self._wait_for_time(distance / speed)
        self._stop_arms()

    def turn_arm_(self, degrees, speed):
        self._start_arms([0], [-speed])
        self._wait_for_time(abs(degrees / speed))
        self._stop_arms()

    # TEMP METHOD
    def grab_object_(self):
        self.open_fingers_()
        self._start_arms([1, 2, 3], [0.25, 0.25, 0.25])
        self._wait_for_time(20)
        self._stop_arms()
        self.close_fingers_()
        self._start_arms([1, 2, 3], [-0.125, -0.125, -0.125])
        self._wait_for_time(30)
        self._stop_arms()

    def open_fingers_(self):
        self._start_fingers(0.1)
        self._wait_for_time(10)
        self._stop_fingers()

    def close_fingers_(self):
        self._start_fingers(-0.0355)
        self._wait_for_time(27)
        self._stop_fingers()


if __name__ == '__main__':
    controller = RobotController(TextRobot, name='Robart')
    controller.drive_forward_(100, 10)
