# reaching out to a server 5 times, in multi-threaded manner

import time
import requests
import threading

THREAD_COUNT = 5

def read_example() -> None:
    response = requests.get('https://www.example.com')
    print(response.status_code)

if __name__ == '__main__':
    sync_start = time.time()
    threads = []
    for i in range(THREAD_COUNT):
        t = threading.Thread(target=read_example)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    sync_end = time.time()
    print(f'Running multithreaded took {sync_end - sync_start:.4f} seconds.') # 0.17s