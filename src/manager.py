import itertools
import logging
import random
from abc import ABC, abstractmethod

from src.eviction import PageIndex, AbstractEvictionPolicy, FrameIndex, NoPage, FIFOEvictionPolicy, LRUEvictionPolicy


class Storage(ABC):
    @abstractmethod
    def load_page(self, page: PageIndex, frame: FrameIndex):
        pass

    @abstractmethod
    def unload_page(self, page: PageIndex, frame: FrameIndex):
        pass


class LoggingStorage(Storage):
    def load_page(self, page: PageIndex, frame: FrameIndex):
        logging.debug("Loading page %i into frame %i", page, frame)

    def unload_page(self, page: PageIndex, frame: FrameIndex):
        logging.debug("Unloading page %i from frame %i", page, frame)


class MemoryManager:
    def __init__(self, storage: Storage, alg: AbstractEvictionPolicy):
        self.alg = alg
        self.storage = storage

    def find_page(self, page: PageIndex) -> FrameIndex:
        cur_page, frame = self.alg.find_page(page)

        if cur_page == NoPage:
            self.storage.load_page(page, frame)
            self.alg.update_mapping(page, frame)
        elif cur_page != page:
            self.storage.unload_page(cur_page, frame)
            self.storage.load_page(page, frame)
            self.alg.update_mapping(page, frame)

        return frame


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s: %(message)s"
    )
    frame_count = 5
    page_count = 12
    mm = MemoryManager(LoggingStorage(), LRUEvictionPolicy(page_count, frame_count))
    for _ in itertools.repeat(None, 100):
        mm.find_page(random.randint(1, page_count))
