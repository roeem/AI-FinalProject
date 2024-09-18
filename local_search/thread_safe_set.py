from threading import Lock
from typing import Any, Iterator


class TSS:
    """
    A thread-safe set implementation.

    This class provides a set-like interface with thread-safe operations for adding and removing elements.
    It uses a threading.Lock to ensure that concurrent access to the underlying set is synchronized.

    Methods:
    - add(element: Any) -> None: Adds an element to the set.
    - remove(element: Any) -> None: Removes an element from the set.
    - __iter__() -> Iterator[Any]: Returns an iterator over the elements of the set.
    """

    def __init__(self):
        """
        Initializes a new thread-safe set.

        Creates an empty set and a lock to ensure thread-safe operations.
        """
        self.__set = set()
        self.__lock = Lock()

    def add(self, element: Any) -> None:
        """
        Adds an element to the set.

        This method acquires a lock to ensure that the addition is thread-safe.

        :param element: The element to be added.
        :type element: Any
        """
        with self.__lock:
            self.__set.add(element)

    def remove(self, element: Any) -> None:
        """
        Removes an element from the set.

        This method acquires a lock to ensure that the removal is thread-safe.

        :param element: The element to be removed.
        :type element: Any
        """
        with self.__lock:
            self.__set.remove(element)

    def __iter__(self) -> Iterator[Any]:
        """
        Returns an iterator over the elements of the set.

        This method returns an iterator for the underlying set.

        :return: An iterator over the elements of the set.
        :rtype: Iterator[Any]
        """
        return self.__set.__iter__()
