from playwright.sync_api import sync_playwright

import queue
import time
import os

from playwright_server.logging.logger import log
from playwright_server.worker.task_manager import manage_task

# Main worker launcher, intended for bullet-proof reliance
# 
# Since the server is reliant on this worker, 
# we need to restart everything and log it if there's an exception.
def worker_backbone(queue):
    """ Main worker function, whose main purpose is stability for our worker. 
    """
    for attempt in range(20):
        try:
            worker(queue)
        except:
            # Nothing to do here, since exception-handling
            # is already done by the worker try-catch block
            # 
            # We just need to restart the worker process
            pass
        else:
            # Break for loop if worker completed without throwing any exception
            break
    else:
        # Will be called if all attempts failed.
        # Python Reference: The else block will NOT be executed if the loop is stopped by a break statement.
        #
        # Kill the app if the state couldn't be recovered within given attempts
        os._exit(1)


def worker(q):
    playwright = None
    browser = None
    task = None

    try:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch()
        while True:
            try:
                task = q.get_task()
                
                result = manage_task(task, browser) or {'error': True, 'content': 'Missing response from worker'}
                result = {
                    "error": False, 
                    "content": "",
                    **result
                }
                q.task_done(task, result)

            except queue.Empty:
                time.sleep(.2)

    except Exception as e:
        print('Exception occurred in Workerthread. Gathering log data and restart worker...')
        log(e)

        # Check if there was an interrupt within an ongoing task.
        # If so, terminate task and report error
        if task:    # Ongoing task? 
            q.task_done(task, {"error": True, "content": "Error ocurred in workerthread"})
        
        # Throw exception to signal an issue for the worker_backbone
        raise Exception('Important! Required to signal worker_backbone there went something wrong')
    finally:
        # Try to close browser and playwright if they are initialized.
        # Might fail too, depending on the exception.
        if browser:
            browser.close()
        if playwright: 
            playwright.stop()