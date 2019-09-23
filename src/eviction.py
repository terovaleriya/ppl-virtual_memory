import logging
import time
from abc import ABC, abstractmethod
from typing import Tuple, Dict

FrameIndex = int
PageIndex = int

NoPage: PageIndex = 0
NoFrame: FrameIndex = 0

# текущяя траница загруженная в кадр и номер кадра
AlgResult = Tuple[PageIndex, FrameIndex]


class AbstractEvictionPolicy(ABC):
    page_count: PageIndex
    frame_count: FrameIndex

    p2f: Dict[PageIndex, FrameIndex]
    f2p: Dict[FrameIndex, PageIndex]

    def __init__(self, page_count: PageIndex, frame_count: FrameIndex):
        self.frame_count = frame_count
        self.page_count = page_count
        self.p2f = {}
        self.f2p = {}

    def find_page(self, page: PageIndex) -> AlgResult:
        logging.debug(self.p2f)
        frame = self.p2f.get(page, NoFrame)
        if frame == NoFrame:
            if len(self.f2p) < self.frame_count:
                page = NoPage
                frame = len(self.f2p) + 1
            else:
                frame = self.next_frame_to_evict()
                page = self.f2p[frame]
        return page, frame

    @abstractmethod
    def next_frame_to_evict(self) -> int:
        pass

    def update_mapping(self, page: PageIndex, frame: FrameIndex) -> None:
        op = self.f2p.get(frame, NoPage)
        if op != page:
            of = self.p2f.get(page, NoFrame)

            if of != NoFrame:
                self.f2p.pop(of)

            if op != NoPage:
                self.p2f.pop(op)

            self.p2f[page] = frame
            self.f2p[frame] = page


class FIFOEvictionPolicy(AbstractEvictionPolicy):
    insertion_index: int = 1

    def __init__(self, page_count: PageIndex, frame_count: FrameIndex):
        super().__init__(page_count, frame_count)

    def next_frame_to_evict(self) -> int:
        frame = self.insertion_index
        self.insertion_index = self.insertion_index + 1
        if self.insertion_index == self.frame_count + 1:
            self.insertion_index = 1
        return frame


class LRUEvictionPolicy(AbstractEvictionPolicy):
    last_used_time: Dict[PageIndex, float] = {}

    def __init__(self, page_count: PageIndex, frame_count: int):
        super().__init__(page_count, frame_count)

    def next_frame_to_evict(self) -> int:
        lru_page = min(self.last_used_time, key=self.last_used_time.get)
        return self.p2f[lru_page]

    def find_page(self, page: PageIndex) -> AlgResult:
        self.last_used_time[page] = time.clock()
        return super().find_page(page)

    def update_mapping(self, page: PageIndex, frame: FrameIndex) -> None:
        op = self.f2p.get(frame, NoPage)
        if op != NoPage and op != page:
            self.last_used_time.pop(op, NoPage)
        super().update_mapping(page, frame)


class OptEvictionPolicy(AbstractEvictionPolicy):
    def __init__(self, page_count: PageIndex, frame_count: FrameIndex):
        super().__init__(page_count, frame_count)

    def next_frame_to_evict(self) -> int:
        return 1
