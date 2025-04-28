from typing import Callable, Generic, TypeVar

import queue
import time
import threading


T = TypeVar('T')


class Worker(threading.Thread, Generic[T]):
    def __init__(self, target: Callable[..., None]) -> None:
        super().__init__()

        self.callback: Callable[..., None] = target
        self.queue: queue.Queue[T] = queue.Queue()

        self._running: bool = False

    def enqueue(self, arguments: T) -> None:
        self.queue.put(arguments)

    def run(self) -> None:
        if self._running:
            return

        self._running = True

        while self._running:
            if not self.queue.empty():
                self.callback(self.queue.get())

            time.sleep(0.25)

    def stop(self, timeout: float | None = None) -> None:
        self._running = False

        self.join(timeout)
