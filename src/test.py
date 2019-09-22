import logging

from src.main import PageAlg, FIFOAlg, LRUAlg, OptAlg, FrameState

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)


#
def test_fifo_alg():
    logging.debug("Running FIFO test")

    alg = FIFOAlg(3, 2)
    assert alg.find_page(1) == (FrameState.EMPTY, 1)
    assert alg.find_page(1) == (FrameState.LOADED, 1)
    assert alg.find_page(2) == (FrameState.EMPTY, 2)
    assert alg.find_page(2) == (FrameState.LOADED, 2)
    assert alg.find_page(3) == (FrameState.REPLACE, 1)
    assert alg.find_page(3) == (FrameState.LOADED, 1)


def test_quick(alg: PageAlg):
    page = alg.find_page(0)
    logging.debug(page)
    assert page == 1


if __name__ == '__main__':
    logging.debug("Running test")

    test_fifo_alg()

    # algs = [FIFOAlg(), LRUAlg(), OptAlg()]
    # for alg in algs:
    #     test_quick(alg)
