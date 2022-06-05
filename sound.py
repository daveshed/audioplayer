import subprocess


class SoundPlayer:
    """Plays sounds using ALSA."""

    def __init__(self, path: str):
        self._path = path
        self._process = None

    def play(self):
        if self._process is None:
            self._process = subprocess.Popen(['aplay', self._path])
            self._process = None
        else:
            self.stop()
            self.play()

    def stop(self):
        if self._process is None:
            return
        self._process.terminate()
