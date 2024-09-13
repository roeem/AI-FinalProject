from threading import Lock
from typing import Any, Iterator


class TSS:
    def __init__(self):
        self.__set = set()
        self.__lock = Lock()

    def add(self, element: Any) -> None:
        with self.__lock:
            self.__set.add(element)

    def remove(self, element: Any) -> None:
        with self.__lock:
            self.__set.remove(element)

    def __iter__(self) -> Iterator[Any]:
        return self.__set.__iter__()
