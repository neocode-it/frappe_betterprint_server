from playwright.sync_api import sync_playwright

import queue
import time

from playwright_server.logging.logger import log

def worker_backbone(queue):
    max_retries = 10
    for attempt in range(max_retries):
        try:
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch()
            worker(queue, browser)
            browser.close()
            playwright.stop()
        except Exception as e:
            print('Exception occurred in Workerthread. Gathering log data and restart worker...')
            log(e)
        else:
            break   # Break for loop if everything done without exception
    else:
        pass    # Final tasks if all attempts failed


