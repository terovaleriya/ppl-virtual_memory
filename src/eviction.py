import logging
from abc import ABC, abstractmethod
from typing import Tuple, Dict

FrameIndex = int
PageIndex = int

NoPage: PageIndex = 0
NoFrame: FrameIndex = 0

# запрошенная страница, текущяя загруженная в кадр страница и номер кадра с которым работать
AlgResult = Tuple[PageIndex, FrameIndex]


class AbstractEvictionPolicy(ABC):
    page_count: PageIndex
    frame_count: FrameIndex

    p2f: Dict[PageIndex, FrameIndex] = {}
    f2p: Dict[FrameIndex, PageIndex] = {}

    def __init__(self, page_count: PageIndex, frame_count: FrameIndex):
        self.frame_count = frame_count
        self.page_count = page_count

    @abstractmethod
    def find_page(self, page: PageIndex) -> AlgResult:
        pass

    def update_mapping(self, page: PageIndex, frame: FrameIndex):
        of = self.p2f.get(page, NoFrame)
        op = self.f2p.get(frame, NoPage)

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

    def find_page(self, page: PageIndex) -> AlgResult:
        frame = self.p2f.get(page, NoFrame)
        if frame == NoFrame:
            if len(self.f2p) < self.frame_count:
                page = NoPage
                frame = len(self.f2p) + 1
            else:
                frame, page = self.insertion_index, self.f2p[self.insertion_index]
                self.insertion_index = self.insertion_index + 1
                if self.insertion_index == self.frame_count + 1:
                    self.insertion_index = 1
        return page, frame


class LRUEvictionPolicy(AbstractEvictionPolicy):
    counter: int = 0

    def __init__(self, page_count: PageIndex, frame_count: int):
        super().__init__(page_count, frame_count)

    def find_page(self, page: PageIndex) -> AlgResult:
        self.counter = self.counter + 1
        return NoPage, self.counter


class OptEvictionPolicy(AbstractEvictionPolicy):
    def __init__(self, page_count: PageIndex, frame_count: FrameIndex):
        super().__init__(page_count, frame_count)

    def find_page(self, page) -> AlgResult:
        pass
