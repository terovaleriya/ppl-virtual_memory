import logging

from src.eviction import AbstractEvictionPolicy, FIFOEvictionPolicy, NoPage, PageIndex, FrameIndex, LRUEvictionPolicy

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)


def check(alg: AbstractEvictionPolicy, page: PageIndex, expected_page: PageIndex, expected_frame: FrameIndex):
    cur_page, frame = alg.find_page(page)

    if cur_page == page:
        logging.debug("We need page #%i and it has been loaded to frame #%i", page, frame)
    elif cur_page == NoPage:
        logging.debug("We need page #%i and we find frame #%i to load it", page, frame)
    else:
        logging.debug("We need page #%i and we get frame #%i to load with currently loaded page #%i", page, frame,
                      cur_page)

    assert cur_page == expected_page, "We expected page " + str(expected_page) + ", but " + str(cur_page) + " received"
    assert frame == expected_frame, "We expected frame " + str(expected_frame) + ", but " + str(frame) + " received"
    alg.update_mapping(page, frame)


def test_fifo_eviction():
    logging.debug("Running FIFO test")

    alg = FIFOEvictionPolicy(13, 2)
    check(alg, 1, NoPage, 1)
    check(alg, 1, 1, 1)
    check(alg, 2, NoPage, 2)
    check(alg, 2, 2, 2)
    check(alg, 3, 1, 1)
    check(alg, 3, 3, 1)
    check(alg, 1, 2, 2)
    check(alg, 1, 1, 2)
    check(alg, 3, 3, 1)

    logging.debug("FIFO test completed")


def test_lru_eviction():
    logging.debug("Running LRU test")

    alg = LRUEvictionPolicy(13, 4)
    check(alg, 1, NoPage, 1)
    check(alg, 1, 1, 1)
    check(alg, 2, NoPage, 2)
    check(alg, 2, 2, 2)
    check(alg, 3, NoPage, 3)
    check(alg, 3, 3, 3)
    check(alg, 4, NoPage, 4)
    check(alg, 1, 1, 1)
    check(alg, 2, 2, 2)
    check(alg, 3, 3, 3)
    check(alg, 1, 1, 1)
    check(alg, 3, 3, 3)
    check(alg, 6, 4, 4)
    check(alg, 7, 2, 2) #
    check(alg, 4, 1, 1)

    logging.debug("LRU test completed")


if __name__ == '__main__':
    logging.debug("Running tests")

    test_fifo_eviction()

    test_lru_eviction()
