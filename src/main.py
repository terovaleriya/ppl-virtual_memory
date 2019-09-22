from typing import Tuple
from abc import ABC, abstractmethod
import logging
from enum import Enum, unique


@unique
class FrameState(Enum):
    EMPTY = 1
    LOADED = 2
    REPLACE = 3


AlgResult = Tuple[FrameState, int]


class PageAlg(ABC):
    def __init__(self, page: int, frame: int):
        self.frame = frame
        self.page = page

    @abstractmethod
    def find_page(self, page) -> AlgResult:
        pass


class FIFOAlg(PageAlg):
    def __init__(self, page: int, frame: int):
        super().__init__(page, frame)

    def find_page(self, page: object) -> AlgResult:
        return FrameState.EMPTY, 1


class LRUAlg(PageAlg):
    counter: int = 0

    def __init__(self, page: int, frame: int):
        super().__init__(page, frame)

    def find_page(self, page) -> AlgResult:
        self.counter = self.counter + 1
        return FrameState.EMPTY, self.counter


class OptAlg(PageAlg):
    def __init__(self, page: int, frame: int):
        super().__init__(page, frame)

    def find_page(self, page) -> AlgResult:
        pass


if __name__ == '__main__':
    logging.debug("Starting application")
    pass
