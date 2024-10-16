from waitress import serve

from filelock import FileLock, Timeout
import threading

from betterprint_server.worker.worker import worker_backbone
from betterprint_server.server.application import application
import betterprint_server.global_queue as global_queue


def start_server(public=False):
    lockfile = "/var/lock/betterprint_server.lock"
    lock = FileLock(lockfile)

    try:
        with lock.acquire(blocking=False):
            print(
                "Serving App on localhost using port 39584. Press Ctrl. + C to stop..."
            )

            # Launch playwright worker thread
            threading.Thread(
                target=worker_backbone, daemon=True, args=(global_queue.queue,)
            ).start()
            threading.Thread(
                target=worker_backbone, daemon=True, args=(global_queue.queue,)
            ).start()

            # Launch http server as interface
            if public:
                serve(application, host="0.0.0.0", port=39584)
            else:
                serve(application, host="127.0.0.1", port=39584)

    except Timeout:
        print(
            "Cannot start server: Another instance of Betterprint Server currently holds the lock."
        )
        exit(1)
