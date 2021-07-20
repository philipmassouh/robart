import json
import math as m
from abc import ABC, abstractmethod
try:
    from webots.controller import Robot
except Exception:
    Robot = object

TIME_STEP = 32
MAX_WHEEL_SPEED = 15.0
WHEEL_SPEED = {
    'max': MAX_WHEEL_SPEED,
    'half': MAX_WHEEL_SPEED / 2.0,
    'quarter': MAX_WHEEL_SPEED / 4.0,
    'eigth': MAX_WHEEL_SPEED / 8.0,
    'sixteenth': MAX_WHEEL_SPEED / 16.0
}
PI_2 = m.pi / 2.0
PI_4 = m.pi / 4.0


def close(current, target, threshold):
    if type(current) is list or type(current) is tuple:
        return all(abs(x - y) < threshold for x, y in zip(current, target))
    return abs(current - target) < threshold


def far(current, target, threshold):
    return not close(current, target, threshold)


def bounded_value(value, bound, offset=0.0):
    if value > bound:
        return -bound + (value - bound) + offset
    elif value < -bound:
        return bound - (-bound - value) - offset
    return value


class AbstractRobot(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def set_gaze_down(self, down, wait): pass

    @abstractmethod
    def turn_left(self, speed): pass

    @abstractmethod
    def turn_right(self, speed): pass

    @abstractmethod
    def face_direction(self, direction): pass

    @abstractmethod
    def drive(self, distance, speed): pass

    @abstractmethod
    def pick_object(self, distance, speed): pass

    @abstractmethod
    def place_object(self, distance, speed): pass


class TextRobot(AbstractRobot):

    def __init__(self, home_coords, name='Robart'):
        super().__init__()
        self.home_coords = home_coords
        self.name = name
        print(f'Initializing at position {home_coords}')

    def set_gaze_down(self, down, wait=True):
        output = f'{self.name}: Looking {"down" if down else "up"}'
        print(output)
        if wait:
            print(f'{self.name}: Waiting')
        return output

    def turn_left(self, speed=WHEEL_SPEED['eigth']):
        output = f'{self.name}: Turning left at speed {speed}'
        print(output)
        return output

    def turn_right(self, speed=WHEEL_SPEED['eigth']):
        output = f'{self.name}: Turning right at speed {speed}'
        print(output)
        return output

    def face_direction(self, direction):
        output = f'{self.name}: Facing direction {direction}'
        print(output)
        return output

    def drive(self, distance, speed=WHEEL_SPEED['half']):
        output = f'{self.name}: Driving distance {distance} at speed {speed}'
        print(output)
        return output

    def pick_object(self, distance=0.205, speed=WHEEL_SPEED['quarter']):
        output = f'{self.name}: Picking object {distance} away at speed {speed}'
        print(output)
        return output

    def place_object(self, distance=0.2025, speed=WHEEL_SPEED['quarter']):
        output = f'{self.name}: Placing object {distance} away at speed {speed}'
        print(output)
        return output


class WebotsRobot(AbstractRobot, Robot):

    def __init__(self, home_coords):
        super().__init__()
        self.coords = self.home_coords = home_coords
        self.direction = self.home_direction = 0
        self.available_torques = [0.0, ] * 8
        self.timestep = int(self.getBasicTimeStep())
        self.m = self._initialize_motors('motors.json')
        self.wheel_motors = self.m['wheel_motors']
        self.rotation_motors = self.m['rotation_motors']
        self.arm_motors = self.m['arm_motors']
        self.hand_motors = self.m['hand_motors']
        self.head_tilt_motor = self.m['body_motors']['head_tilt']
        self.torso_lift_motor = self.m['body_motors']['torso_lift']
        self.s = self._initialize_sensors('sensors.json')
        self.camera_sensors = self.s['camera_sensors']
        self.contact_sensors = self.s['contact_sensors']
        self.wheel_sensors = self.s['wheel_sensors']
        self.rotation_sensors = self.s['rotation_sensors']
        self.arm_sensors = self.s['arm_sensors']
        self.hand_sensors = self.s['hand_sensors']
        self.head_tilt_sensor = self.s['body_sensors']['head_tilt']
        self.torso_lift_sensor = self.s['body_sensors']['torso_lift']
        self.compass = self.s['body_sensors']['compass']
        self.gps = self.s['body_sensors']['gps']
        self.inertial_unit = self.s['body_sensors']['inertial_unit']
        self._initialize_robot()

    def _initialize_motors(self, motors_file):
        with open(motors_file) as f:
            m = json.load(f)
        for motors in m.values():
            for key, value in motors.items():
                motors[key] = self.getDevice(value)
                if 'wheel' in key:
                    motors[key].setPosition(float('inf'))
                    motors[key].setVelocity(0.0)
        return m

    def _initialize_sensors(self, sensors_file):
        with open(sensors_file) as f:
            s = json.load(f)
        for sensors in s.values():
            for key, value in sensors.items():
                sensors[key] = self.getDevice(value)
                sensors[key].enable(self.timestep)
        for name, motors in self.m.items():
            name = name.split('_')[0] + '_sensors'
            s[name] = {} if name not in s.keys() else s[name]
            for key, value in motors.items():
                s[name][key] = value.getPositionSensor()
                s[name][key].enable(self.timestep)
        return s

    def _initialize_robot(self):
        self.set_gaze_down(True, wait=False)
        self._set_arm_position(True, 0.0, 1.35, 0.0, -2.2, 0.0, wait=False)
        self._set_arm_position(False, 0.0, 1.35, 0.0, -2.2, 0.0, wait=True)
        self._set_hand_closed(True, False, wait=False)
        self._set_hand_closed(False, False, wait=True)

    def _wait(self, time):
        step = 0
        while self.step(self.timestep) != -1 and step < time:
            step += 1

    def _set_motors_positions(self, motors, positions, torque=None):
        if not torque:
            torque = list(motors)[0].getAvailableTorque()
        for motor, position in zip(motors, positions):
            motor.setAvailableTorque(torque)
            motor.setPosition(position)

    def _set_motors_position(self, motors, position, torque=None):
        self._set_motors_positions(motors, ((position, )*len(motors)), torque)

    def _set_wheels_speeds(self, fll, flr, frl, frr, bll, blr, brl, brr):
        targets = (fll, flr, frl, frr, bll, blr, brl, brr)
        for wheel, speed in zip(self.wheel_motors.values(), targets):
            wheel.setVelocity(speed)

    def _set_wheels_speed(self, speed):
        self._set_wheels_speeds(*((speed, )*8))

    def _set_wheels_rotations(self, fl, fr, bl, br, wait=True):
        if wait:
            self._set_wheels_speed(0.0)
            self._set_wheels_passive(True)
        targets = (fl, fr, bl, br)
        self._set_motors_positions(self.rotation_motors.values(), targets)
        if wait:
            test_sensor, test_target = self.rotation_sensors['fl'], targets[0]
            while far(test_sensor.getValue(), test_target, 0.05):
                self.step(self.timestep)
            self._set_wheels_passive(False)

    def _set_wheels_rotation(self, rotation, wait=True):
        self._set_wheels_rotations(*((rotation, )*4), wait)

    def _set_wheels_passive(self, passive):
        if passive:
            for index, wheel in enumerate(self.wheel_motors.values()):
                self.available_torques[index] = wheel.getAvailableTorque()
                wheel.setAvailableTorque(0.0)
        else:
            for index, wheel in enumerate(self.wheel_motors.values()):
                wheel.setAvailableTorque(self.available_torques[index])

    def _set_robot_rotation(self, angle, speed):
        self._set_wheels_rotations(3.0 * PI_4, PI_4, -3.0 * PI_4, -PI_4)
        rotation = self.inertial_unit.getRollPitchYaw()[2]
        target = bounded_value(rotation + angle, m.pi, 0.025)
        wheel_speed = speed if angle > 0 else -speed
        self._set_wheels_speed(wheel_speed)
        while far(rotation, target, 0.005):
            self.step(self.timestep)
            rotation = self.inertial_unit.getRollPitchYaw()[2]
            if close(rotation, target, 0.05):
                self._set_wheels_speed(wheel_speed / 16.0)
        self._set_wheels_rotation(0.0)

    def _set_arm_speeds(self, left, sp, sl, ar, ef, wr):
        motors = [value for key, value in self.arm_motors.items()
                  if key.startswith('l' if left else 'r')]
        targets = (sp, sl, ar, ef, wr)
        for motor, velocity in zip(motors, targets):
            motor.setVelocity(velocity)

    def _set_arm_position(self, left, sp, sl, ar, ef, wr, wait=True):
        motors = [value for key, value in self.arm_motors.items()
                  if key.startswith('l' if left else 'r')]
        sensors = [value for key, value in self.arm_sensors.items()
                   if key.startswith('l' if left else 'r')]
        targets = (sp, sl, ar, ef, wr)
        for motor, position in zip(motors, targets):
            motor.setPosition(position)
        self._set_arm_speeds(left, 1.5, 1.5, 1.5, 2.5, 1.5)
        while wait and far([s.getValue() for s in sensors], targets, 0.05):
            self.step(self.timestep)

    def _set_hand_closed(self, left, closed, torque=10.0, wait=True):
        motors = [value for key, value in self.hand_motors.items()
                  if key.startswith('l' if left else 'r')]
        positions = [value for key, value in self.hand_sensors.items()
                     if key.startswith('l' if left else 'r')]
        contacts = [value for key, value in self.contact_sensors.items()
                    if key.startswith('l' if left else 'r')]
        target = 0.0 if closed else 0.5
        self._set_motors_position(motors, target)
        while wait and far(positions[0].getValue(), target, 0.05):
            if closed and all(sensor.getValue() > 0.5 for sensor in contacts):
                position = max(0.0, 0.95 * positions[0].getValue())
                self._set_motors_position(motors, position, torque)
                break
            self.step(self.timestep)

    def _set_robot_alignment(self, alignment, direction):
        def comparison(x, y): return x > y if direction in (0, 3) else x < y
        target, result = (0, 2) if direction in (0, 2) else (2, 0)
        if comparison(self.gps.getValues()[target], alignment[target]):
            self._set_wheels_rotations(0.025, 0.025, 0.0, 0.0, False)
        else:
            self._set_wheels_rotations(-0.025, -0.025, 0.0, 0.0, False)
        return self.gps.getValues()[result]

    def _get_position_target(self, direction, distance):
        axis = 0 if direction in (1, 3) else 1
        distance = -distance if direction in (0, 1) else distance
        position = self.coords[axis]
        return position, position + distance

    def set_gaze_down(self, down, wait=True):
        target = 0.5 if down else 0.0
        self.head_tilt_motor.setPosition(target)
        while wait and far(self.head_tilt_sensor.getValue(), target, 0.05):
            self.step(self.timestep)

    def turn_left(self, speed=WHEEL_SPEED['eigth']):
        self._set_robot_rotation(PI_2, speed)
        if self.direction < 3:
            self.direction += 1
        else:
            self.direction = 0

    def turn_right(self, speed=WHEEL_SPEED['eigth']):
        self._set_robot_rotation(-PI_2, speed)
        if self.direction > 0:
            self.direction -= 1
        else:
            self.direction = 3

    def turn_around(self, speed=WHEEL_SPEED['eigth']):
        self._set_robot_rotation(m.pi, speed)
        if self.direction < 2:
            self.direction += 2
        else:
            self.direction -= 2

    def face_direction(self, direction):
        if self.direction - direction in (-1, 3):
            self.turn_left()
        elif self.direction - direction in (1, -3):
            self.turn_right()
        elif self.direction - direction in (-2, 2):
            self.turn_around()

    def drive(self, distance, speed=WHEEL_SPEED['half']):
        alignment = self.gps.getValues()
        position, target = self._get_position_target(self.direction, distance)
        wheel_speed = speed if distance > 0 else -speed
        self._set_wheels_speed(wheel_speed)
        while far(position, target, 0.0025):
            position = self._set_robot_alignment(alignment, self.direction)
            if close(position, target, 0.1):
                self._set_wheels_speed(wheel_speed / 16.0)
            self.step(self.timestep)
        self.coords = (self.gps.getValues()[0], self.gps.getValues()[2])
        self._set_wheels_speed(0.0)

    def pick_object(self, distance=0.1995, speed=WHEEL_SPEED['quarter']):
        self._set_arm_position(True, 0.0, 1.1, 0.0, -1.1, 0.0)
        self.drive(distance, speed)
        self._wait(25)
        self._set_hand_closed(True, True)
        self._wait(25)
        self._set_arm_position(True, 0.0, 0.85, 0.0, -1.25, 0.0, True)
        self.drive(-distance, speed)

    def place_object(self, distance=0.195, speed=WHEEL_SPEED['quarter']):
        self.drive(distance, speed)
        self._wait(25)
        self._set_arm_position(True, 0.0, 1.1, 0.0, -1.11, 0.0)
        self._wait(25)
        self._set_hand_closed(True, False)
        self.drive(-distance, speed)
        self._set_arm_position(True, 0.0, 1.35, 0.0, -2.2, 0.0)

    def goto_coords(self, coords, speed=WHEEL_SPEED['half']):
        self.set_gaze_down(False)
        if far(self.coords[1], coords[1], 0.125):
            self.face_direction(1 if self.coords[0] > 6.0 else 3)
            self.drive(abs(self.coords[0] - 6.0), speed)
            self.face_direction(0 if self.coords[1] > coords[1] else 2)
            self.drive(abs(self.coords[1] - coords[1]), speed)
        self.face_direction(1 if self.coords[0] > coords[0] else 3)
        self.drive(abs(self.coords[0] - coords[0]), speed)
        self.face_direction(0 if coords == self.home_coords else 2)
        self.set_gaze_down(True)


class RobotController:

    def __init__(self, robot: AbstractRobot, home_coords):
        self.robot = robot(home_coords=home_coords)
        self.home_coords = home_coords
        methods = {method: getattr(self.robot, method) for method in dir(
            self.robot) if not method.startswith('_')}
        self.__dict__.update(methods)
        self.stored_coords = None

    def __getattr__(self, name):
        return getattr(self.robot, name)

    def return_item(self, return_home=True):
        if self.stored_coords:
            self.pick_object()
            self.goto_coords(self.stored_coords)
            self.place_object()
            if return_home:
                self.goto_coords(self.home_coords)
            self.stored_coords = None
        else:
            print('Robart: Nothing to return :(')

    def get_at_coords(self, coords):
        self.return_item(False)
        self.goto_coords(coords)
        self.pick_object()
        self.goto_coords(self.home_coords)
        self.place_object()
        self.stored_coords = coords


if __name__ == '__main__':
    library = {
        'can': [4, -1],
        'water': [1, -1],
        'apple': [-2, -1],
        'orange': [-5, -1],
        'bottle': [4, 1],
        'extinguisher': [1, 1],
        'paint': [-2, 1],
        'gnome': [-5, 1],
        'crackers': [4, 3],
        'cereal': [1, 3],
        'honey': [-2, 3],
        'jam': [-5, 3],
        'cup': [4, 5],
        'flowers': [1, 5],
        'tree': [-2, 5],
        'trash': [-5, 5],
        'duck': [4, 7]
    }
    robot = RobotController(WebotsRobot, home_coords=(8.0, -1.0))
    robot.get_at_coords(library['water'])
    robot.get_at_coords(library['extinguisher'])
    robot.get_at_coords(library['bottle'])
    robot.return_item()
