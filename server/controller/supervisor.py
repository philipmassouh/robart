import os
import time
from subprocess import PIPE, Popen

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

items = ['honey', 'water', 'flowers', 'orange']
robots = {
    'Robot1': {
        'x': 7.4,
        'y': -1.0,
        'cols': (-1.0, 1.0),
        'items': []
    },
    'Robot2': {
        'x': 8.6,
        'y': -1.0,
        'cols': (3.0, 5.0),
        'items': []
    }
}


for item in items:
    for robot in robots.values():
        if library[item][1] in robot['cols']:
            robot['items'].append(item)
            break

for name, robot in robots.items():
    if len(robot['items']) > 0:
        os.environ['WEBOTS_ROBOT_NAME'] = name
        x, y, items = robot['x'], robot['y'], robot['items']
        Popen(
            f'py controllers.py -n {name} -x {x} -y {y} -i {" ".join(items)}')
