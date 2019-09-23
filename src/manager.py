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
    def __init__(self, name: str):
        self.name = name

    def load_page(self, page: PageIndex, frame: FrameIndex):
        logging.debug("Loading page %i into frame %i in storage %s", page, frame, self.name)

    def unload_page(self, page: PageIndex, frame: FrameIndex):
        logging.debug("Unloading page %i from frame %i in storage %s", page, frame, self.name)


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
        else:
            logging.debug("Page %i already loaded to frame %i", page, frame)
        return frame


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s: %(message)s"
    )
    frame_count = 5
    page_count = 12

    logging.debug("We run FIFO memory manager")
    m0 = MemoryManager(LoggingStorage("M0"), FIFOEvictionPolicy(page_count, frame_count))
    for _ in itertools.repeat(None, 100):
        m0.find_page(random.randint(1, page_count))

    logging.debug("\n\n########################\n\n")
    logging.debug("We run LRU memory manager")
    m1 = MemoryManager(LoggingStorage("M1"), LRUEvictionPolicy(page_count, frame_count))
    for _ in itertools.repeat(None, 100):
        m1.find_page(random.randint(1, page_count))