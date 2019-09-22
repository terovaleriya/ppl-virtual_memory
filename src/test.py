import logging

from src.main import PageAlg, FIFOAlg, LRUAlg, OptAlg

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)


def test_quick(alg: PageAlg):
    page = alg.find_page(0)
    logging.debug(page)
    assert page == 1


if __name__ == '__main__':
    logging.debug("Running test")
    algs = [FIFOAlg(), LRUAlg(), OptAlg()]
    for alg in algs:
        test_quick(alg)
