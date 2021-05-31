"""demo_controller controller."""

from webots.controller import Robot, Keyboard, PositionSensor, Motor

# Constants.
TIME_STEP = 32
WMAX_VEL = 14.81
AMAX_VEL = 1.5708


class DemoController:

    def __init__(self):
        self.robot = Robot()
        self.timestep = int(self.robot.getBasicTimeStep())
        self.running = True
        self.arms = [
            self.robot.getDevice('arm1'),
            self.robot.getDevice('arm2'),
            self.robot.getDevice('arm3'),
            self.robot.getDevice('arm4'),
            self.robot.getDevice('arm5')
        ]
        self.fingers = [
            self.robot.getDevice('finger1'),
            self.robot.getDevice('finger2')
        ]
        self.wheels = [
            self.robot.getDevice('wheel1'),
            self.robot.getDevice('wheel2'),
            self.robot.getDevice('wheel3'),
            self.robot.getDevice('wheel4')
        ]
        self.get_item = {
            'cube': lambda: self.get_item_1(),
            'computer': lambda: self.get_item_3(),
            'box': lambda: self.get_item_4(),
            'place': lambda: self.place_item()
        }
        self._configure_robot()
        self._initialize_robot()

    def _configure_robot(self):
        # Lets arms be set by velocity.
        for arm in self.arms:
            arm.setPosition(float('inf'))

        # Lets all the fingers be set by velocity.
        for finger in self.fingers:
            finger.setPosition(float('inf'))

        # Lets wheels be set by velocity.
        for wheel in self.wheels:
            wheel.setPosition(float('inf'))

    def _initialize_robot(self):
        self.wheels_stop()
        self.arms_stop()
        self.fingers_stop()
        self.align_robot()

    def arms_rotate(self, arms, speeds):
        for arm, speed in zip(arms, speeds):
            self.arms[arm].setVelocity(speed * AMAX_VEL)

    def arms_stop(self):
        for arm in self.arms:
            arm.setVelocity(0)

    def fingers_move(self, speed):
        for finger in self.fingers:
            finger.setVelocity(speed * 0.1)

    def fingers_stop(self):
        for finger in self.fingers:
            finger.setVelocity(0)

    def wheels_drive(self, speed):
        for wheel in self.wheels:
            wheel.setVelocity(speed * WMAX_VEL)

    def wheels_strafe(self, speed):
        self.wheels[0].setVelocity(speed * -WMAX_VEL)
        self.wheels[1].setVelocity(speed * WMAX_VEL)
        self.wheels[2].setVelocity(speed * WMAX_VEL)
        self.wheels[3].setVelocity(speed * -WMAX_VEL)

    def wheels_turn(self, speed):
        self.wheels[0].setVelocity(speed * WMAX_VEL)
        self.wheels[1].setVelocity(speed * -WMAX_VEL)
        self.wheels[2].setVelocity(speed * WMAX_VEL)
        self.wheels[3].setVelocity(speed * -WMAX_VEL)

    def wheels_stop(self):
        for wheel in self.wheels:
            wheel.setVelocity(0)

    def align_robot(self):
        local_step = 0
        while self.robot.step(self.timestep) != -1 and self.running:
            if local_step == 10:
                self.arms_rotate((1, 2, 3), (1, -1, 1))
            elif local_step == 50:
                self.arms_stop()
            elif local_step == 60:
                self.wheels_turn(1)
            elif local_step == 92:
                self.wheels_stop()
            elif local_step == 100:
                self.wheels_drive(1)
            elif local_step == 260:
                self.wheels_stop()
            elif local_step == 290:
                self.running = False
            local_step += 1

    def get_item_1(self):
        local_step = 0
        while self.robot.step(self.timestep) != -1 and self.running:
            if local_step == 0:
                self.wheels_turn(1)
            elif local_step == 32:
                self.wheels_stop()
            elif local_step == 40:
                self.wheels_drive(1)
            elif local_step == 252:
                self.wheels_stop()
            elif local_step == 280:
                self.wheels_turn(-1)
            elif local_step == 312:
                self.wheels_stop()
            elif local_step == 340:
                self.wheels_drive(1)
            elif local_step == 376:
                self.wheels_stop()
                self.fingers_move(0.12)
                self.arms_rotate([1, 3], [-0.85, -0.725])
            elif local_step == 440:
                self.arms_stop()
                self.fingers_stop()
            elif local_step == 450:
                self.fingers_move(-0.12)
            elif local_step == 514:
                self.fingers_stop()
            elif local_step == 520:
                self.arms_rotate([1, 3], [0.85, 0.8])
            elif local_step == 584:
                self.arms_stop()
            elif local_step == 590:
                self.fingers_move(0.5)
            elif local_step == 600:
                self.fingers_stop()
            elif local_step == 610:
                self.wheels_drive(-1)
            elif local_step == 650:
                self.wheels_stop()
            elif local_step == 676:
                self.wheels_turn(1)
            elif local_step == 708:
                self.wheels_stop()
            elif local_step == 738:
                self.wheels_drive(-1)
            elif local_step == 960:
                self.wheels_stop()
            elif local_step == 990:
                self.wheels_turn(-1)
            elif local_step == 1022:
                self.wheels_stop()
            elif local_step == 1040:
                self.running = False
            local_step += 1

    def get_item_3(self):
        local_step = 0
        while self.robot.step(self.timestep) != -1 and self.running:
            if local_step == 0:
                self.wheels_strafe(-0.98)
                self.fingers_move(-1)
            elif local_step == 5:
                self.fingers_stop()
                self.arms_rotate([0], [1])
            elif local_step == 10:
                self.arms_stop()
            elif local_step == 13:
                self.wheels_stop()
            elif local_step == 15:
                self.fingers_move(1)
            elif local_step == 18:
                self.fingers_stop()
            elif local_step == 20:
                self.wheels_drive(1)
            elif local_step == 25:
                self.arms_rotate([3], [-1])
            elif local_step == 30:
                self.arms_stop()
            elif local_step == 35:
                self.arms_rotate([0, 3], [-1, 1])
            elif local_step == 40:
                self.arms_stop()
            elif local_step == 59:
                self.wheels_stop()
            elif local_step == 60:
                self.arms_rotate([1, 3], [-0.78, -0.96])
            elif local_step == 120:
                self.arms_stop()
            elif local_step == 145:
                self.fingers_move(-1)
            elif local_step == 155:
                self.arms_rotate([1, 3], [0.78, 0.96])
            elif local_step == 160:
                self.fingers_stop()
            elif local_step == 215:
                self.arms_stop()
            elif local_step == 230:
                self.fingers_move(1)
            elif local_step == 233:
                self.fingers_stop()
            elif local_step == 240:
                self.wheels_drive(-1)
            elif local_step == 272:
                self.wheels_stop()
            elif local_step == 300:
                self.running = False
            local_step += 1

    def get_item_4(self):
        local_step = 0
        while self.robot.step(self.timestep) != -1 and self.running:
            if local_step == 0:
                self.wheels_strafe(1)
                self.fingers_move(-1)
            elif local_step == 5:
                self.fingers_stop()
                self.arms_rotate([0], [-1])
            elif local_step == 10:
                self.arms_stop()
            elif local_step == 15:
                self.fingers_move(1)
            elif local_step == 18:
                self.fingers_stop()
            elif local_step == 25:
                self.arms_rotate([3], [-1])
            elif local_step == 30:
                self.arms_stop()
            elif local_step == 35:
                self.arms_rotate([0, 3], [1, 1])
            elif local_step == 40:
                self.arms_stop()
            elif local_step == 140:
                self.wheels_stop()
            elif local_step == 160:
                self.wheels_drive(1)
            elif local_step == 192:
                self.wheels_stop()
            elif local_step == 200:
                self.arms_rotate([1, 3], [-0.98, -0.9])
            elif local_step == 255:
                self.arms_stop()
                self.fingers_move(-1)
            elif local_step == 270:
                self.fingers_stop()
            elif local_step == 275:
                self.arms_rotate([1, 3], [0.98, 0.9])
            elif local_step == 329:
                self.arms_stop()
            elif local_step == 365:
                self.fingers_move(1)
            elif local_step == 368:
                self.fingers_stop()
            elif local_step == 370:
                self.arms_rotate([1, 3], [0.98, 0.9])
            elif local_step == 371:
                self.arms_stop()
            elif local_step == 400:
                self.wheels_drive(-1)
            elif local_step == 432:
                self.wheels_stop()
            elif local_step == 450:
                self.wheels_strafe(-1)
            elif local_step == 590:
                self.wheels_stop()
            elif local_step == 620:
                self.running = False
            local_step += 1

    def place_item(self):
        local_step = 0
        while self.robot.step(self.timestep) != -1 and self.running:
            if local_step == 0:
                self.arms_rotate([0, 1], [-0.135, -0.2])
                self.wheels_strafe(1)
            elif local_step == 40:
                self.arms_stop()
            elif local_step == 50:
                self.arms_rotate([2, 1], [1, -0.2])
            elif local_step == 85:
                self.arms_stop()
                self.fingers_move(-1)
            elif local_step == 100:
                self.fingers_stop()
                self.wheels_stop()
                self.arms_rotate([1], [-1])
            elif local_step == 120:
                self.wheels_drive(1)
                self.arms_stop()
            elif local_step == 157:
                self.wheels_stop()
            elif local_step == 160:
                self.fingers_move(-0.1)
                self.arms_rotate([0, 1, 3], [-1, 0.5, -0.1])
            elif local_step == 218:
                self.arms_stop()
            elif local_step == 220:
                self.fingers_move(1)
            elif local_step == 222:
                self.fingers_stop()
            elif local_step == 230:
                self.wheels_drive(-1)
            elif local_step == 240:
                self.arms_rotate([0, 1, 3], [1, -0.5, 0.1])
            elif local_step == 267:
                self.wheels_stop()
            elif local_step == 298:
                self.arms_stop()
                self.arms_rotate([1], [1])
                self.wheels_strafe(-1)
            elif local_step == 318:
                self.arms_rotate([2, 1], [-1, 0.2])
            elif local_step == 353:
                self.arms_rotate([0, 1, 2], [0.135, 0.2, 0])
            elif local_step == 393:
                self.arms_stop()
            elif local_step == 398:
                self.wheels_stop()
            local_step += 1

    def run(self, item):
        self.running = True
        self.get_item[item]()
