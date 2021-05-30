import pyaudio
import wave


class Recorder:
    def __init__(self, max_sec=5):

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

    def set_listening(self, listening):

        self.listening = listening

    # Pass in a function that returns true when audio recording should stop
    def record(self, app=None):
        print("---RECORDING---")

        self.frames = []

        i = 0
        while self.listening and i < int(self.rate_hz / self.chunk_size * self.max_seconds):
            if app:
                app.processEvents()
            data = self.stream.read(self.chunk_size)
            self.frames.append(data)
            i += 1

        print("---DONE RECORDING---")

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

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


''' 

EXAMPLE USAGE

r = Recorder()
frames = r.record(quitOnKeypress) # where quitOnKeypress is externally defined
r.send_to_file()

'''
