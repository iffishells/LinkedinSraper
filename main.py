import threading
from scraper import Linkedin

HEADLESS = False
NUM_CHROMES = 2


def worker():
    L = Linkedin('uc', headless2=HEADLESS, start=True)
    L.open_links()


def main():
    threads = []

    for _ in range(NUM_CHROMES):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
