import math as m
# import time as t
from abc import ABC, abstractmethod
try:
    from webots.controller import Robot
except Exception as identifier:
    Robot = object


TIME_STEP = 64
MAX_WHEEL_SPEED = 15.0
HALF_WHEEL_SPEED = MAX_WHEEL_SPEED / 2.0
QUARTER_WHEEL_SPEED = MAX_WHEEL_SPEED / 4.0
EIGHTH_WHEEL_SPEED = MAX_WHEEL_SPEED / 8.0
SIXTEENTH_WHEEL_SPEED = MAX_WHEEL_SPEED / 16.0
WHEELS_DISTANCE = 0.4492
SUB_WHEELS_DISTANCE = 0.098
WHEEL_RADIUS = 0.08
PI_4 = m.pi / 4.0


class RobotController:

    def __init__(self, robot, name=None):
        self.robot = robot(name=name) if name else robot()
        methods = {method: getattr(self.robot, method) for method in
                   dir(self.robot) if not method.startswith('_')}
        self.__dict__.update(methods)
        self.object_distances = {
            'obj1': 120,
            'obj2': 240,
        }
        self.placement = 15

    def __getattr__(self, name):
        return getattr(self.robot, name)

    def get_object_(self, object):
        self.robot.drive_forward_(self.object_distances[object], 0.5)
        self.robot.raise_arm_(20, 0.8)
        self.robot.turn_arm_(-30, 0.8)
        self.robot.grab_object_()
        self.robot.turn_arm_(-30, -0.8)
        self.robot.lower_arm_(20, 0.25)
        self.robot.store_object_()
        self.robot.drive_backward_(self.object_distances[object], 0.5)
        self.robot.place_object_(self.placement)
        self.placement += 5


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


class WebotsRobot(Robot):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.timestep = int(self.getBasicTimeStep())
        self.fl_wheel_motors = {
            'left': self.getDevice('fl_caster_l_wheel_joint'),
            'right': self.getDevice('fl_caster_r_wheel_joint')
        }
        self.fl_wheel_sensors = {
            'left': self.fl_wheel_motors['left'].getPositionSensor(),
            'right': self.fl_wheel_motors['right'].getPositionSensor()
        }
        self.fr_wheel_motors = {
            'left': self.getDevice('fr_caster_l_wheel_joint'),
            'right': self.getDevice('fr_caster_r_wheel_joint')
        }
        self.fr_wheel_sensors = {
            'left': self.fr_wheel_motors['left'].getPositionSensor(),
            'right': self.fr_wheel_motors['right'].getPositionSensor()
        }
        self.bl_wheel_motors = {
            'left': self.getDevice('bl_caster_l_wheel_joint'),
            'right': self.getDevice('bl_caster_r_wheel_joint')
        }
        self.bl_wheel_sensors = {
            'left': self.bl_wheel_motors['left'].getPositionSensor(),
            'right': self.bl_wheel_motors['right'].getPositionSensor()
        }
        self.br_wheel_motors = {
            'left': self.getDevice('br_caster_l_wheel_joint'),
            'right': self.getDevice('br_caster_r_wheel_joint')
        }
        self.br_wheel_sensors = {
            'left': self.br_wheel_motors['left'].getPositionSensor(),
            'right': self.br_wheel_motors['right'].getPositionSensor()
        }
        self.wheel_motors = list(self.fl_wheel_motors.values()) + \
            list(self.fr_wheel_motors.values()) + \
            list(self.bl_wheel_motors.values()) + \
            list(self.br_wheel_motors.values())
        self.wheel_sensors = list(self.fl_wheel_sensors.values()) + \
            list(self.fr_wheel_sensors.values()) + \
            list(self.bl_wheel_sensors.values()) + \
            list(self.br_wheel_sensors.values())
        self.rotation_motors = {
            'front_left': self.getDevice('fl_caster_rotation_joint'),
            'front_right': self.getDevice('fr_caster_rotation_joint'),
            'back_left': self.getDevice('bl_caster_rotation_joint'),
            'back_right': self.getDevice('br_caster_rotation_joint')
        }
        self.rotation_sensors = {
            'front_left': self.rotation_motors['front_left'].getPositionSensor(),
            'front_right': self.rotation_motors['front_right'].getPositionSensor(),
            'back_left': self.rotation_motors['back_left'].getPositionSensor(),
            'back_right': self.rotation_motors['back_right'].getPositionSensor()
        }
        self.left_arm_motors = {
            'shoulder_pan': self.getDevice('l_shoulder_pan_joint'),
            'shoulder_lift': self.getDevice('l_shoulder_lift_joint'),
            'upper_roll': self.getDevice('l_upper_arm_roll_joint'),
            'elbow_flex': self.getDevice('l_elbow_flex_joint'),
            'wrist_roll': self.getDevice('l_wrist_roll_joint')
        }
        self.right_arm_motors = {
            'shoulder_pan': self.getDevice('r_shoulder_pan_joint'),
            'shoulder_lift': self.getDevice('r_shoulder_lift_joint'),
            'upper_roll': self.getDevice('r_upper_arm_roll_joint'),
            'elbow_flex': self.getDevice('r_elbow_flex_joint'),
            'wrist_roll': self.getDevice('r_wrist_roll_joint'),
        }
        self.left_arm_sensors = {
            'shoulder_pan': self.left_arm_motors['shoulder_pan'].getPositionSensor(),
            'shoulder_lift': self.left_arm_motors['shoulder_lift'].getPositionSensor(),
            'upper_roll': self.left_arm_motors['upper_roll'].getPositionSensor(),
            'elbow_flex': self.left_arm_motors['elbow_flex'].getPositionSensor(),
            'wrist_roll': self.left_arm_motors['wrist_roll'].getPositionSensor()
        }
        self.right_arm_sensors = {
            'shoulder_pan': self.right_arm_motors['shoulder_pan'].getPositionSensor(),
            'shoulder_lift': self.right_arm_motors['shoulder_lift'].getPositionSensor(),
            'upper_roll': self.right_arm_motors['upper_roll'].getPositionSensor(),
            'elbow_flex': self.right_arm_motors['elbow_flex'].getPositionSensor(),
            'wrist_roll': self.right_arm_motors['wrist_roll'].getPositionSensor()
        }
        self.left_hand_motors = {
            'left_finger': self.getDevice('l_gripper_l_finger_joint'),
            'right_finger': self.getDevice('l_gripper_r_finger_joint'),
            'left_tip': self.getDevice('l_gripper_l_finger_tip_joint'),
            'right_tip': self.getDevice('l_gripper_r_finger_tip_joint')
        }
        self.right_hand_motors = {
            'left_finger': self.getDevice('r_gripper_l_finger_joint'),
            'right_finger': self.getDevice('r_gripper_r_finger_joint'),
            'left_tip': self.getDevice('r_gripper_l_finger_tip_joint'),
            'right_tip': self.getDevice('r_gripper_r_finger_tip_joint')
        }
        self.body_motors = {
            'head_tilt': self.getDevice('head_tilt_joint'),
            'torso_lift': self.getDevice('torso_lift_joint')
        }
        self.body_sensors = {
            'head_tilt': self.body_motors['head_tilt'].getPositionSensor(),
            'torso_lift': self.body_motors['torso_lift'].getPositionSensor()
        }
        self.cameras = {
            'left_arm': self.getDevice('l_forearm_cam_sensor'),
            'right_arm': self.getDevice('r_forearm_cam_sensor'),
            'left_eye': self.getDevice('wide_stereo_l_stereo_camera_sensor'),
            'right_eye': self.getDevice('wide_stereo_r_stereo_camera_sensor')
        }
        self.left_hand_sensors = {
            'left_contact': self.getDevice('l_gripper_l_finger_tip_contact_sensor'),
            'right_contact': self.getDevice('l_gripper_r_finger_tip_contact_sensor'),
            'left_finger': self.left_hand_motors['left_finger'].getPositionSensor(),
            'right_finger': self.left_hand_motors['right_finger'].getPositionSensor(),
            'left_tip': self.left_hand_motors['left_tip'].getPositionSensor(),
            'right_tip': self.left_hand_motors['right_tip'].getPositionSensor()
        }
        self.right_hand_sensors = {
            'left_contact': self.getDevice('r_gripper_l_finger_tip_contact_sensor'),
            'right_contact': self.getDevice('r_gripper_r_finger_tip_contact_sensor'),
            'left_finger': self.right_hand_motors['left_finger'].getPositionSensor(),
            'right_finger': self.right_hand_motors['right_finger'].getPositionSensor(),
            'left_tip': self.right_hand_motors['left_tip'].getPositionSensor(),
            'right_tip': self.right_hand_motors['right_tip'].getPositionSensor()
        }
        self.inertial_unit = self.getDevice('inertial unit')
        self.gps = self.getDevice('gps')
        self.compass = self.getDevice('compass')
        self.available_torques = [0.0, ] * 8
        self.current_coords = [8.0, -1.0]
        self.home_coords = [8.0, -1.0]
        self.current_direction = 0
        self.home_direction = 0
        self.stored_coords = None
        self._initialize()

    def _initialize(self):
        for wheel in self.wheel_motors:
            wheel.setPosition(float('inf'))
            wheel.setVelocity(0.0)
        for sensor in self.wheel_sensors:
            sensor.enable(TIME_STEP)
        for sensor in self.rotation_sensors.values():
            sensor.enable(TIME_STEP)
        for camera in self.cameras.values():
            camera.enable(TIME_STEP)
        for sensor in self.left_arm_sensors.values():
            sensor.enable(TIME_STEP)
        for sensor in self.right_arm_sensors.values():
            sensor.enable(TIME_STEP)
        for sensor in self.left_hand_sensors.values():
            sensor.enable(TIME_STEP)
        for sensor in self.right_hand_sensors.values():
            sensor.enable(TIME_STEP)
        for sensor in self.body_sensors.values():
            sensor.enable(TIME_STEP)
        for camera in self.cameras.values():
            camera.enable(TIME_STEP)
            # camera.recognitionEnable(TIME_STEP)
        self.inertial_unit.enable(TIME_STEP)
        self.gps.enable(TIME_STEP)
        self.compass.enable(TIME_STEP)
        self._set_initial_positions()

    def _set_initial_positions(self):
        self._toggle_gaze(True, False)
        self._set_arm_position(True, 0.0, 1.35, 0.0, -2.2, 0.0, False)
        self._set_arm_position(False, 0.0, 1.35, 0.0, -2.2, 0.0, False)
        self._toggle_gripper(True, True, 0.0, False)
        self._toggle_gripper(False, True, 0.0, True)

    def _wait_for_time(self, time):
        step = 0
        while self.step(self.timestep) != -1 and step < time:
            step += 1

    def _set_wheels_speeds(self, fll, flr, frl, frr, bll, blr, brl, brr):
        self.fl_wheel_motors['left'].setVelocity(fll)
        self.fl_wheel_motors['right'].setVelocity(flr)
        self.fr_wheel_motors['left'].setVelocity(frl)
        self.fr_wheel_motors['right'].setVelocity(frr)
        self.bl_wheel_motors['left'].setVelocity(bll)
        self.bl_wheel_motors['right'].setVelocity(blr)
        self.br_wheel_motors['left'].setVelocity(brl)
        self.br_wheel_motors['right'].setVelocity(brr)

    def _set_wheels_speed(self, speed):
        self._set_wheels_speeds(*((speed,) * 8))

    def _stop_wheels(self):
        self._set_wheels_speeds(*((0.0,) * 8))

    def _toggle_passive_wheels(self, enable):
        if enable:
            for index, wheel in enumerate(self.wheel_motors):
                self.available_torques[index] = wheel.getAvailableTorque()
                wheel.setAvailableTorque(0.0)
        else:
            for index, wheel in enumerate(self.wheel_motors):
                wheel.setAvailableTorque(self.available_torques[index])

    def _set_wheels_rotation(self, fl, fr, bl, br, wait):
        if wait:
            self._stop_wheels()
            self._toggle_passive_wheels(True)
        self.rotation_motors['front_left'].setPosition(fl)
        self.rotation_motors['front_right'].setPosition(fr)
        self.rotation_motors['back_left'].setPosition(bl)
        self.rotation_motors['back_right'].setPosition(br)
        if wait:
            target = [fl, fr, bl, br]
            targets_reached = False
            while not targets_reached:
                for index, sensor in enumerate(self.rotation_sensors.values()):
                    current_position = sensor.getValue()
                    if abs(current_position - target[index]) < 0.05:
                        targets_reached = True
                self.step(self.timestep)
            self._toggle_passive_wheels(False)

    def _robot_rotate(self, angle, speed):
        self._stop_wheels()
        self._set_wheels_rotation(3.0 * PI_4, PI_4, -3.0 * PI_4, -PI_4, True)
        wheel_speed = speed if angle > 0 else -speed
        current_orientation = self.inertial_unit.getRollPitchYaw()[2]
        target_orientation = current_orientation + angle
        if target_orientation > m.pi:
            target_orientation = -m.pi + (target_orientation - m.pi) + 0.025
        elif target_orientation < -m.pi:
            target_orientation = m.pi - (-m.pi - target_orientation) - 0.025
        self._set_wheels_speed(wheel_speed)
        while abs(target_orientation - current_orientation) > 0.005:
            current_orientation = self.inertial_unit.getRollPitchYaw()[2]
            if abs(target_orientation - current_orientation) < 0.05:
                self._set_wheels_speed(wheel_speed / 16.0)
            self.step(self.timestep)
        self._stop_wheels()
        self.step(self.timestep)
        self._set_wheels_rotation(*((0.0,) * 4), True)

    def _face_direction(self, direction):
        if direction == 0:
            if self.current_direction == 1:
                self.turn_right()
            elif self.current_direction == 2:
                self.turn_around()
            elif self.current_direction == 3:
                self.turn_left()
        elif direction == 1:
            if self.current_direction == 0:
                self.turn_left()
            elif self.current_direction == 2:
                self.turn_right()
            elif self.current_direction == 3:
                self.turn_around()
        elif direction == 2:
            if self.current_direction == 0:
                self.turn_around()
            elif self.current_direction == 1:
                self.turn_left()
            elif self.current_direction == 3:
                self.turn_right()
        else:
            if self.current_direction == 0:
                self.turn_right()
            elif self.current_direction == 1:
                self.turn_around()
            elif self.current_direction == 2:
                self.turn_left()

    def _set_arm_position(self, left, shoulder_pan, shoulder_lift,
                          upper_roll, elbow_flex, wrist_roll, wait):
        if left:
            motors = self.left_arm_motors
            sensors = self.left_arm_sensors
        else:
            motors = self.right_arm_motors
            sensors = self.right_arm_sensors
        motors['shoulder_pan'].setPosition(shoulder_pan)
        motors['shoulder_lift'].setPosition(shoulder_lift)
        motors['upper_roll'].setPosition(upper_roll)
        motors['elbow_flex'].setPosition(elbow_flex)
        motors['wrist_roll'].setPosition(wrist_roll)
        for motor in motors.values():
            motor.setVelocity(1.5)
        motors['elbow_flex'].setVelocity(2.5)
        if wait:
            while abs(sensors['shoulder_pan'].getValue() - shoulder_pan) > 0.05 or \
                    abs(sensors['shoulder_lift'].getValue() - shoulder_lift) > 0.05 or \
                    abs(sensors['upper_roll'].getValue() - upper_roll) > 0.05 or \
                    abs(sensors['elbow_flex'].getValue() - elbow_flex) > 0.05 or \
                    abs(sensors['wrist_roll'].getValue() - wrist_roll) > 0.05:
                self.step(self.timestep)

    def _toggle_gripper(self, left, open, torque, wait):
        if left:
            motors = self.left_hand_motors
            sensors = self.left_hand_sensors
        else:
            motors = self.right_hand_motors
            sensors = self.right_hand_sensors
        maxTorque = motors['left_finger'].getAvailableTorque()
        for motor in motors.values():
            motor.setAvailableTorque(maxTorque)
        if open:
            targetValue = 0.5
            for motor in motors.values():
                motor.setPosition(targetValue)
            while wait and abs(sensors['left_finger'].getValue() - targetValue) > 0.05:
                self.step(self.timestep)
        else:
            targetValue = 0.0
            for motor in motors.values():
                motor.setPosition(targetValue)
            while wait and (sensors['left_contact'].getValue() < 0.5 or
                            sensors['right_contact'].getValue() < 0.5) and \
                    abs(sensors['left_finger'].getValue() - targetValue) > 0.05:
                self.step(self.timestep)
            current_position = sensors['left_finger'].getValue()
            for motor in motors.values():
                motor.setAvailableTorque(torque)
                motor.setPosition(max(0.0, 0.95 * current_position))

    def _toggle_gaze(self, down, wait):
        if down:
            target_position = 0.5
        else:
            target_position = 0.0
        self.body_motors['head_tilt'].setPosition(target_position)
        while wait and abs(self.body_sensors['head_tilt'].getValue() - target_position) > 0.05:
            self.step(self.timestep)

    def turn_left(self, speed=EIGHTH_WHEEL_SPEED):
        self._robot_rotate(m.pi / 2.0, speed)
        self.current_direction += 1
        if self.current_direction > 3:
            self.current_direction = 0

    def turn_right(self, speed=EIGHTH_WHEEL_SPEED):
        self._robot_rotate(-m.pi / 2.0, speed)
        self.current_direction -= 1
        if self.current_direction < 0:
            self.current_direction = 3

    def turn_around(self, speed=EIGHTH_WHEEL_SPEED):
        self._robot_rotate(m.pi, speed)
        if self.current_direction == 0:
            self.current_direction = 2
        elif self.current_direction == 2:
            self.current_direction = 0
        elif self.current_direction == 1:
            self.current_direction = 3
        elif self.current_direction == 3:
            self.current_direction = 1

    def drive(self, distance, speed=HALF_WHEEL_SPEED):
        initial_wheel_position = self.fl_wheel_sensors['left'].getValue()
        wheel_travel_distane = 0
        alignment = self.gps.getValues()[0] \
            if self.current_direction in (0, 2) else self.gps.getValues()[2]
        wheel_speed = speed if distance > 0 else -speed
        self._set_wheels_speed(wheel_speed)
        if self.current_direction == 0:
            current_position = self.current_coords[1]
            target_position = self.current_coords[1] - distance
        elif self.current_direction == 2:
            current_position = self.current_coords[1]
            target_position = self.current_coords[1] + distance
        elif self.current_direction == 1:
            current_position = self.current_coords[0]
            target_position = self.current_coords[0] - distance
        elif self.current_direction == 3:
            current_position = self.current_coords[0]
            target_position = self.current_coords[0] + distance
        while abs(target_position - current_position) > 0.0025:
            wheel_position = self.fl_wheel_sensors['left'].getValue()
            wheel_travel_distane = abs(WHEEL_RADIUS * (wheel_position - initial_wheel_position))
            if self.current_direction == 0:
                if self.gps.getValues()[0] > alignment:
                    self._set_wheels_rotation(0.025, 0.025, 0.0, 0.0, False)
                else:
                    self._set_wheels_rotation(-0.025, -0.025, 0.0, 0.0, False)
                current_position = self.gps.getValues()[2]
            elif self.current_direction == 2:
                if self.gps.getValues()[0] < alignment:
                    self._set_wheels_rotation(0.025, 0.025, 0.0, 0.0, False)
                else:
                    self._set_wheels_rotation(-0.025, -0.025, 0.0, 0.0, False)
                current_position = self.gps.getValues()[2]
            elif self.current_direction == 1:
                if self.gps.getValues()[2] < alignment:
                    self._set_wheels_rotation(0.025, 0.025, 0.0, 0.0, False)
                else:
                    self._set_wheels_rotation(-0.025, -0.025, 0.0, 0.0, False)
                current_position = self.gps.getValues()[0]
            elif self.current_direction == 3:
                if self.gps.getValues()[2] > alignment:
                    self._set_wheels_rotation(0.025, 0.025, 0.0, 0.0, False)
                else:
                    self._set_wheels_rotation(-0.025, -0.025, 0.0, 0.0, False)
                current_position = self.gps.getValues()[0]
            if abs(distance) - wheel_travel_distane < 0.1:
                self._set_wheels_speed(wheel_speed / 16.0)
            self.step(self.timestep)
        self._stop_wheels()
        self.current_coords = [self.gps.getValues()[0]] + [self.gps.getValues()[2]]

    def goto_coords(self, coords, speed=HALF_WHEEL_SPEED):
        self._toggle_gaze(False, True)
        if coords == self.home_coords:
            self.turn_left()
            if self.current_coords[0] < coords[0] - 0.5:
                self._face_direction(3)
                self.drive(abs(self.current_coords[0] - coords[0]), speed)
            elif self.current_coords[0] > coords[0] + 0.5:
                self._face_direction(1)
                self.drive(abs(self.current_coords[0] - coords[0]), speed)
            if self.current_coords[1] < coords[1] - 0.5:
                self._face_direction(2)
                self.drive(abs(self.current_coords[1] - coords[1]), speed)
            elif self.current_coords[1] > coords[1] + 0.5:
                self._face_direction(0)
                self.drive(abs(self.current_coords[1] - coords[1]), speed)
            self._face_direction(0)
        elif abs(self.current_coords[1] - coords[1]) > 1:
            self.turn_left()
            self.drive(abs(self.current_coords[0] - 6), speed)
            if self.current_coords[1] < coords[1] - 0.5:
                self._face_direction(2)
                self.drive(abs(self.current_coords[1] - coords[1]), speed)
            elif self.current_coords[1] > coords[1] + 0.5:
                self._face_direction(0)
                self.drive(abs(self.current_coords[1] - coords[1]), speed)
            if self.current_coords[0] < coords[0] - 0.5:
                self._face_direction(3)
                self.drive(abs(self.current_coords[0] - coords[0]), speed)
            elif self.current_coords[0] > coords[0] + 0.5:
                self._face_direction(1)
                self.drive(abs(self.current_coords[0] - coords[0]), speed)
            self._face_direction(2)
        else:
            if self.current_coords[1] < coords[1] - 0.5:
                self._face_direction(2)
                self.drive(abs(self.current_coords[1] - coords[1]), speed)
            elif self.current_coords[1] > coords[1] + 0.5:
                self._face_direction(0)
                self.drive(abs(self.current_coords[1] - coords[1]), speed)
            if self.current_coords[0] < coords[0] - 0.5:
                self._face_direction(3)
                self.drive(abs(self.current_coords[0] - coords[0]), speed)
            elif self.current_coords[0] > coords[0] + 0.5:
                self._face_direction(1)
                self.drive(abs(self.current_coords[0] - coords[0]), speed)
            self._face_direction(2)
        self._toggle_gaze(True, True)

    def grab_object(self):
        self._set_arm_position(True, 0.0, 1.1, 0.0, -1.1, 0.0, True)
        self.drive(0.205, QUARTER_WHEEL_SPEED)
        self._wait_for_time(25)
        self._toggle_gripper(True, False, 10, True)
        self._wait_for_time(25)
        self._set_arm_position(True, 0.0, 0.85, 0.0, -1.25, 0.0, True)
        # self._set_arm_position(True, 0.0, 0.85, 0.0, -1.25, 1.57, True)
        self.drive(-0.205, QUARTER_WHEEL_SPEED)

    def place_object(self):
        self.drive(0.2025, QUARTER_WHEEL_SPEED)
        self._wait_for_time(25)
        self._set_arm_position(True, 0.0, 1.1, 0.0, -1.1, 0.0, True)
        self._wait_for_time(25)
        self._toggle_gripper(True, True, 10, True)
        self.drive(-0.2025, QUARTER_WHEEL_SPEED)
        self._set_arm_position(True, 0.0, 1.35, 0.0, -2.2, 0.0, True)

    def get_at_coords(self, coords):
        if self.stored_coords:
            self.return_item(False)
        self.stored_coords = coords
        self.goto_coords(coords)
        self.grab_object()
        self.goto_coords(self.home_coords)
        self.place_object()

    def return_item(self, return_home=True):
        if self.stored_coords:
            self.grab_object()
            self.goto_coords(self.stored_coords)
            self.place_object()
            if return_home:
                self.goto_coords(self.home_coords)
            self.stored_coords = None
        else:
            print('Robard: Nothing to return :(')


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
    robot = RobotController(WebotsRobot, name='Robart')
    robot.get_at_coords(library['bottle'])
    robot.get_at_coords(library['tree'])
    robot.get_at_coords(library['flowers'])
    robot.get_at_coords(library['apple'])
    robot.get_at_coords(library['can'])
    robot.return_item()
