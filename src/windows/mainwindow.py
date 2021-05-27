'''
Created by: Craig Fouts
Created on: 5/25/2021
'''

import os
from configparser import ConfigParser
from pathlib import Path
from PySide6.QtUiTools import QUiLoader
from stt.record import Recorder
from stt.watson_stt import SpeechToText
from windows.window import Window

PROJECT_PATH = Path().resolve()
CONFIG_PATH = os.path.join(PROJECT_PATH, 'config', 'config.ini')

config = ConfigParser()
config.read(CONFIG_PATH)
loader = QUiLoader()
stt = SpeechToText()
recorder = Recorder()


class MainWindow(Window):
    '''TODO

    '''

    def __init__(self, *args, **kwargs):
        ui_path = os.path.join(PROJECT_PATH, 'views', 'mainwindow.ui')
        super().__init__(ui_path, *args, **kwargs)

        self._configure_window()

    def _configure_window(self):
        '''TODO

        '''

        self._configure_callbacks()

    def _configure_callbacks(self):
        '''TODO

        '''

        self.ui.listen_btn.clicked.connect(self._handle_listen)
        self.ui.run_btn.clicked.connect(self._handle_run)

    def _handle_listen(self):
        '''TODO

        '''

        frames, rate, channels = recorder.record()
        instruction = stt.recognize_speech(frames, rate, channels)
        self.ui.instruction_inp.setText(instruction[0]['transcript'])

    def _handle_run(self):
        '''TODO

        '''

        print('RUN')
