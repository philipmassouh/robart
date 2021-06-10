'''
Created by: Craig Fouts
Created on: 6/10/2021
'''


class AdapterController:

    def __init__(self, robot):
        self.robot = robot()
        methods = {method: getattr(self.robot, method) for method in
                   dir(self.robot) if not method.startswith('_')}
        self.__dict__.update(methods)

    def __getattr__(self, name):
        return getattr(self.robot, name)


class TestRobot:

    def say(self, text):
        print(text)


if __name__ == '__main__':
    controller = AdapterController(TestRobot)
    controller.say('Hello, World')
