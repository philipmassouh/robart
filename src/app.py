'''
Created by: Craig Fouts, Noah LaPolt, Philip Massouh, Dennis Sweeney
Created on: 5/22/2021
'''

import os
import sys
from configparser import ConfigParser
from windows.mainwindow import MainWindow
from pathlib import Path
from PySide6.QtWidgets import QApplication

PROJECT_PATH = Path().resolve()
CONFIG_PATH = os.path.join(PROJECT_PATH, 'config', 'config.ini')

config = ConfigParser()
config.read(CONFIG_PATH)


class Application(QApplication):
    '''TODO

    '''

    def __init__(self, window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.window = window(self)
        self.window.show_()


def start():
    '''TODO

    '''

    app_window = MainWindow
    app = Application(app_window, sys.argv)
    app.exec()


if __name__ == '__main__':
    start()
