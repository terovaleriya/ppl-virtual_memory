from typing import Tuple
from abc import ABC, abstractmethod
import logging

AlgResult = Tuple[bool, int]


class PageAlg(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def find_page(self, page) -> AlgResult:
        pass


class FIFOAlg(PageAlg):
    def __init__(self):
        super().__init__()

    def find_page(self, page: object) -> AlgResult:
        return True, 5


class LRUAlg(PageAlg):
    counter: int = 0

    def __init__(self):
        super().__init__()

    def find_page(self, page) -> AlgResult:
        self.counter = self.counter + 1
        return True, self.counter


class OptAlg(PageAlg):
    def __init__(self):
        super().__init__()

    def find_page(self, page) -> AlgResult:
        pass


if __name__ == '__main__':
    logging.debug("Starting application")
    pass
