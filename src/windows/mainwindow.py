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

    def __init__(self, app, *args, **kwargs):
        super().__init__('main', *args, **kwargs)

        self.app = app
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

        self._toggle_listen_btn()
        frames, rate, channels = recorder.record(self.app)
        recorder.send_to_file(os.path.join('output', 'output.wav'))
        instruction = stt.recognize_speech(frames, rate, channels)
        if instruction:
            self.ui.instruction_inp.setText(instruction[0]['transcript'])

    def _handle_stop_listening(self):
        '''TODO

        '''

        self._toggle_listen_btn()
        recorder.set_listening(False)
        self.app.processEvents()

    def _toggle_listen_btn(self):
        '''TODO

        '''

        self.ui.listen_btn.clicked.disconnect()
        if self.ui.listen_btn.text() == 'Listen':
            self._set_listen()
        else:
            self._set_stop_listening()

    def _set_listen(self):
        '''TODO

        '''

        self.ui.listen_btn.setText('Stop Listening')
        self.ui.listen_btn.clicked.connect(self._handle_stop_listening)
        self.ui.instruction_inp.setEnabled(False)
        self.ui.run_btn.setEnabled(False)

    def _set_stop_listening(self):
        '''TODO

        '''

        self.ui.listen_btn.setText('Listen')
        self.ui.listen_btn.clicked.connect(self._handle_listen)
        self.ui.instruction_inp.setEnabled(True)
        self.ui.run_btn.setEnabled(True)

    def _handle_run(self):
        '''TODO

        '''

        print('RUN')
