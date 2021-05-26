'''
Created by: Craig Fouts
Created on: 5/25/2021
'''

import os
from configparser import ConfigParser
from pathlib import Path
from PySide6.QtUiTools import QUiLoader
from windows.window import Window

PROJECT_PATH = Path().resolve()
CONFIG_PATH = os.path.join(PROJECT_PATH, 'config', 'config.ini')

config = ConfigParser()
config.read(CONFIG_PATH)
loader = QUiLoader()


class MainWindow(Window):
    '''TODO

    '''

    def __init__(self, *args, **kwargs):
        ui_path = os.path.join(PROJECT_PATH, 'views', 'mainwindow.ui')
        super().__init__(ui_path, *args, **kwargs)
