import time


class Timer:
    def __init__(self):
        self._start_time = None
        self._elapsed_time = 0
        self.running = False

        self._solving_start_time = None
        self._solving_elapsed_time = 0
        self._solving_running = False

    @property
    def elapsed_time(self):
        if self.running:
            return self._elapsed_time + (time.time() - self._start_time)
        return self._elapsed_time

    @property
    def solving_elapsed_time(self):
        if self.solving_running:
            return self._solving_elapsed_time + (time.time() - self._solving_start_time)
        return self._elapsed_time

    @property
    def formatted_time(self):
        elapsed = self.elapsed_time
        minutes, seconds = divmod(elapsed, 60)
        return f"{int(minutes):02}:{int(seconds):02}"

    def start(self):
        if not self.running:
            self._start_time = time.time()
            self.running = True

    def stop(self):
        if self.running:
            self._elapsed_time += time.time() - self._start_time
            self.running = False
            self._stop_solving()

    def reset(self):
        self._start_time = None
        self._elapsed_time = 0
        self.running = False
        self._reset_solving()

    def start_solving(self):
        if not self.solving_running:
            self._solving_start_time = time.time()
            self._solving_running = True

    def _stop_solving(self):
        if self.solving_running:
            self._solving_elapsed_time += time.time() - self._solving_start_time
            self.solving_running = False

    def _reset_solving(self):
        self._solving_start_time = None
        self._solving_elapsed_time = 0
        self.solving_running = False
