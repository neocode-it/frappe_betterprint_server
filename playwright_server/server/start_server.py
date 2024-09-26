from waitress import serve

from filelock import FileLock, Timeout
import threading

from playwright_server.worker.worker import worker_backbone
from playwright_server.server.application import application
import playwright_server.global_queue as global_queue


def start_server(public=False):
    lockfile = '/var/lock/playwright_server.lock'
    lock = FileLock(lockfile)

    try:
        
        with lock.acquire(blocking=False):
            print('Serving App on localhost using port 39584. Press Ctrl. + C to stop...')

            # Launch playwright worker thread
            threading.Thread(target=worker_backbone, daemon=True, args=(global_queue.queue,)).start()
            threading.Thread(target=worker_backbone, daemon=True, args=(global_queue.queue,)).start()


    except Timeout:
        print("Cannot start server: Another instance of Playwright Server currently holds the lock.")
        exit(1)