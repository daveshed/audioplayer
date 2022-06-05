import threading
import time


class SwitchPoller(threading.Thread):
    """Polls the input at the specified frequency in a thread.

    Invokes the callback then the state has changed.
    """
    POLL_HZ = 10

    def __init__(self, read_state, callback):
        self._read_state = read_state
        self._callback = callback
        self._quit = threading.Event()
        super().__init__(name=type(self).__name__)

    def run(self):
        last_state = self._read_state()
        while not self._quit.is_set():
            time.sleep(1 / self.POLL_HZ)
            new_state = self._read_state()
            if last_state != new_state:
                print('Activated' if new_state else 'Deactivated')
                self._callback(new_state)
                last_state = new_state
        print("terminated")

    def stop(self):
        self._quit.set()
