'''
Created by: Craig Fouts
Created on: 5/25/2021
'''

import os
from configparser import ConfigParser
from pathlib import Path
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow

PROJECT_PATH = Path().resolve()
CONFIG_PATH = os.path.join(PROJECT_PATH, 'config', 'config.ini')

config = ConfigParser()
config.read(CONFIG_PATH)
loader = QUiLoader()


class Window(QMainWindow):
    '''TODO

    '''

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = os.path.join(PROJECT_PATH, config.get('UI Files', name))
        ui_file = QFile(ui_path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        icon_path = os.path.join(PROJECT_PATH, config.get('Icons', name))
        icon_file = QIcon(icon_path)
        self.ui.setWindowIcon(icon_file)

    def resize_and_center(self, width, height):
        '''TODO

        '''

        self.ui.resize(width, height)
        frame = self.ui.frameGeometry()
        screen_center = self.screen.availableGeometry().center()
        frame.moveCenter(screen_center)
        self.ui.move(frame.topLeft())

    def show_(self):
        '''TODO

        '''

        self.ui.show()
