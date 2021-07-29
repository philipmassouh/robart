from controllers import RobotController, WebotsRobot
import numpy as np
import math as m
import time
import json


class Walk:
    def __init__(self):
        self.SIZE = 256
        self.FIND_OBJECTS = 2
        self.sku = 0
        self.world = {
            'first': [['ground']*self.SIZE]*self.SIZE,
            'second': [['ground']*self.SIZE]*self.SIZE,
            'third': [['ground']*self.SIZE]*self.SIZE,
            'forth': [['ground']*self.SIZE]*self.SIZE,
            'center': ''
        }
        self.objects = {}
        self.robot = RobotController(WebotsRobot, name='Robart')
        self.cameras = [self.robot.cameras['camera'], self.robot.cameras['left_eye'], self.robot.cameras['right_eye']]
        self.dim = [
            (self.cameras[0].getHeight(), self.cameras[0].getWidth()),
            (self.cameras[1].getHeight(), self.cameras[1].getWidth()),
            (self.cameras[2].getHeight(), self.cameras[2].getWidth())
        ]
        self.cameras[0].recognitionEnable(self.robot.timestep)
        self.cameras[0].enableRecognitionSegmentation()

    # Returns the image or a specific color of the image.
    def getImage(self, device, rgba=-1):
        if rgba > -1 and rgba < 4:
            return self.getImage(device)[:,:,rgba]
        else:
            # Numpy array of the current image.
            return np.frombuffer(self.cameras[device].getImage(), dtype=np.uint8).reshape(self.dim[device][0], self.dim[device][1], 4)

    def catalog(self):
        # Saves an image of what the robot sees.
        #self.cameras[0].getRecognitionSegmentationImage()
        #self.cameras[0].saveRecognitionSegmentationImage("tester.png", 100)

        self.robot._set_wheels_rotation(3.0 * m.pi / 4.0, m.pi / 4.0, -3.0 * m.pi / 4.0, -m.pi / 4.0, True)
        self.robot._set_wheels_speed(10)

        time.sleep(2)

        i = 0
        while i < self.FIND_OBJECTS:
            # Takes a step in the sim.
            self.robot.step(self.robot.timestep)

            # Loops through all objects and checks if it knows about them.
            for obj in self.cameras[0].getRecognitionObjects():
                # Calculates object position and color.
                color = obj.get_colors()
                object_pos_cam = np.add(np.array(obj.get_position()), np.array([0.10789, 0, 0.12197]))
                object_pos_wrd = np.around(np.subtract(np.array(self.robot.gps.getValues()), object_pos_cam)).astype(np.int32).tolist()
                object_name = obj.get_model().decode("utf-8")

                # Determinds the object found based on color.
                if color[0] == 1 and self.get_object(object_pos_wrd) != 'wall':
                    self.add_object((object_pos_wrd, 'wall'))
                elif color[1] == 1 and (len(self.get_object(object_pos_wrd)) == 0 or (len(self.get_object(object_pos_wrd)) == 2 and object_name not in self.get_object(object_pos_wrd)[1])):
                    # Adds object to world and objects dict.
                    self.add_object((object_pos_wrd, ('table', [object_name])))

                    # Initializes model if it has not found it yet.
                    if object_name not in self.objects:
                        self.objects[object_name] = {'count': 0, 'entities': []}

                    # Updates object values.
                    self.objects[object_name]['count'] += 1
                    self.objects[object_name]['entities'].append({'pos': [object_pos_wrd[0], object_pos_wrd[2]], 'sku': self.sku})
                    self.sku += 1

                    # Found an object.
                    i += 1

                elif color[0] == 0.5 and len(self.get_object(object_pos_wrd)) != 2:
                    self.add_object((object_pos_wrd, ('table', [])))

        # Saves the objects found into the database.
        self.robot._set_wheels_speed(0)
        self.save_database()

    # Saves the database.
    def save_database(self):
        database = {
            'freeSpace': [],
            'nextSKU': self.sku + 1,
            'objects': self.objects,
            'table': []
        }

        with open('./server/server/data.json', 'w') as outfile:
            json.dump(database, outfile, indent=4)
            outfile.close()


    # Adds an object to the world.
    def add_object(self, obj):
        x = obj[0][0]
        z = obj[0][2]

        # Prevent out of bounds errors.
        if np.abs(x) > self.SIZE or np.abs(z) > self.SIZE:
            return -1

        # Updates item in world.
        if x > 0 and z > 0:
            if type(obj[1]) is tuple:
                if len(self.world['first'][x][z]) == 2:
                    if len(obj[1][1][0]) != 0:
                        self.world['first'][x][z][1].append(obj[1][1][0])
                else:
                    self.world['first'][x][z] = obj[1]
            else:
                self.world['first'][x][z] = obj[1]
        elif x < 0 and z > 0:
            if type(obj[1]) is tuple:
                if len(self.world['second'][-x][z]) == 2:
                    if len(obj[1][1][0]) != 0:
                        self.world['second'][-x][z][1].append(obj[1][1][0])
                else:
                    self.world['second'][-x][z] = obj[1]
            else:
                self.world['second'][-x][z] = obj[1]
        elif x < 0 and z < 0:
            if type(obj[1]) is tuple:
                if len(self.world['third'][-x][-z]) == 2:
                    if len(obj[1][1][0]) != 0:
                        print(self.world['third'][-x][-z][1])
                        self.world['third'][-x][-z][1].append(obj[1][1][0])
                else:
                    self.world['third'][-x][-z] = obj[1]
            else:
                self.world['third'][-x][-z] = obj[1]
        elif x > 0 and z < 0:
            if type(obj[1]) is tuple:
                if len(self.world['forth'][x][-z]) == 2:
                    if len(obj[1][1][0]) != 0:
                        self.world['forth'][x][-z][1].append(obj[1][1][0])
                else:
                    self.world['forth'][x][-z] = obj[1]
            else:
                self.world['forth'][x][-z] = obj[1]
        elif x == 0 and z == 0:
            if type(obj[1]) is tuple:
                if len(self.world['center']) == 2:
                    if len(obj[1][1][0]) != 0:
                        self.world['center'][1].append(obj[1][1][0])
                else:
                    self.world['center'] = obj[1]
            else:
                self.world['center'] = obj[1]
        else:
            return -1

        return 0

    # Returns the object in the requested pos.
    def get_object(self, pos):
        x = pos[0]
        z = pos[2]

        # Prevent out of bounds errors.
        if np.abs(x) > self.SIZE or np.abs(z) > self.SIZE:
            return 'ground'

        if x > 0 and z > 0:
            return self.world['first'][x][z]
        elif x < 0 and z > 0:
            return self.world['second'][-x][z]
        elif x < 0 and z < 0:
            return self.world['third'][-x][-z]
        elif x > 0 and z < 0:
            return self.world['forth'][x][-z]
        else:
            return self.world['center']
        

if __name__ == "__main__":
    walk = Walk()
    walk.catalog()