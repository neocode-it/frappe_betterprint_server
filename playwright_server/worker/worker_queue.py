import threading
import queue
import uuid

class WorkerQueue:
    _result = {}
    _result_condition = threading.Condition()

    _q = queue.Queue()
    
    def run_and_wait(self, command : str, content : dict = {}):
        key = uuid.uuid4()
        self._q.put({
            "key": key,
            "command": command,
            **content
        })

        with self._result_condition:
            while not key in self._result:
                self._result_condition.wait()
            result = self._result[key]
            self._result.pop(key)
            return result

    def get_task(self):
        return self._q.get(timeout=1)

    def task_done(self, task, result):
        with self._result_condition:
            self._result[task["key"]] = result
            self._result_condition.notify_all()