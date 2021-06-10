'''# EXAMPLE USAGE

r = Recorder()
frames = r.record(quitOnKeypress) # where quitOnKeypress is externally defined
r.send_to_file()

'''


import pyaudio
import wave


class Recorder:
    def __init__(self, max_sec=5, pyaudio=pyaudio):

        # Max recording size if user doesn't stop
        self.max_seconds = max_sec

        # Changing these is not recommended
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt16
        self.num_channels = 1
        self.rate_hz = 44100

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=self.audio_format,
                                  channels=self.num_channels,
                                  rate=self.rate_hz,
                                  input=True,
                                  frames_per_buffer=self.chunk_size)

        self.listening = True

    def stop_listening(self):
        self.listening = False

    def record(self, app=None):
        print("---RECORDING---")

        self.frames = []

        self.listening = True

        limit = int(self.rate_hz / self.chunk_size * self.max_seconds)
        for i in range(limit):
            if app:
                app.processEvents()
                if not self.listening:
                    break
            data = self.stream.read(self.chunk_size)
            self.frames.append(data)

        print("---DONE RECORDING---")

        # returns (frames, rate, channels)
        return (b''.join(self.frames), self.rate_hz, self.num_channels)

    # Outputs as file for debugging purposes
    def send_to_file(self, output_file="output.wav"):
        wf = wave.open(output_file, 'wb')
        wf.setnchannels(self.num_channels)
        wf.setsampwidth(self.p.get_sample_size(self.audio_format))
        wf.setframerate(self.rate_hz)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    # Closes the input audio stream
    def close_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
