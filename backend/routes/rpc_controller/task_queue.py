import time
import threading
from queue import Queue
from  .controller import RpcController

# Singleton design of queue to prevent multiple instances of the queue. This 
# buffers the tasks assigned to Rpc Controller.
class TaskQueue:
    task_queue = Queue()
    controller = RpcController()
    master_thread = None
    historical_task_result = {}

    @staticmethod
    def add_task(task):
        TaskQueue.task_queue.put_nowait(task)

        # First time initialization
        if TaskQueue.master_thread is None:
            # Submit the initial task to controller
            TaskQueue.controller.init_task(TaskQueue.task_queue.get_nowait())

            # Initialize the thread
            master_thread = threading.Thread(target=TaskQueue.feed_task)
            master_thread.start()

    @staticmethod
    def get_task_result(video_identifier):
        return TaskQueue.historical_task_result[video_identifier]

    @staticmethod
    def feed_task():
        while True:
            if TaskQueue.task_queue.empty():
                time.sleep()
                continue

            task_status = TaskQueue.controller.get_task()
            if task_status["State"] == "RUNNING":
                time.sleep()
                continue
            
            if task_status["State"] == "COMPLETED":
                TaskQueue.historical_task_result[task_status["Input_Video_Path"]] = task_status

            task = TaskQueue.task_queue.get_nowait()
            TaskQueue.controller.init_task(task)
