from typing import Callable

import time
import threading


class Repeater(threading.Thread):
    def __init__(
        self,
        target: Callable[..., None],
        interval: float = 0.25
    ) -> None:
        super().__init__()

        self.callback: Callable[..., None] = target
        self.interval: float = interval

        self._running: bool = False

    def run(self) -> None:
        if self._running:
            return

        self._running = True

        while self._running:
            self.callback()
            time.sleep(self.interval)

    def stop(self, timeout: float | None = None) -> None:
        self._running = False

        self.join(timeout)
