from modules.stt.record import Recorder
from types import SimpleNamespace


class MockPyAudio:
    def __init__(self):
        self.opened = False
        self.terminated = False

    def open(self, *args, **kwargs):
        self.opened = True

        class Stream:
            def read(self, chunk_size):
                return b'F'

            def stop_stream(self):
                pass

            def close(self):
                pass

        return Stream()

    def terminate(self):
        self.terminated = True


mock_pyaudio = SimpleNamespace(PyAudio=MockPyAudio, paInt16="paInt16")


class MockApp:

    def __init__(self, recorder):
        self.recorder = recorder
        self.state = 0

    def processEvents(self):
        if self.state == 10:
            self.recorder.toggle_listening()
        else:
            self.state += 1


def test_recorder():
    r = Recorder(pyaudio=mock_pyaudio)
    assert r.p.opened

    data1, rate, channels = r.record()
    assert len(data1) > 0
    assert data1 == b'F' * len(data1)

    assert not r.close_stream()

    mock_app = MockApp(r)
    data2, rate, channels = r.record(mock_app)
    assert len(data2) > 0
    assert data2 == b'F' * len(data2)

    assert len(data2) < len(data1)
