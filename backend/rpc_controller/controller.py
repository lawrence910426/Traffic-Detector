class RpcController:
    controller_state = None

    @staticmethod
    def init_task():
        RpcController.controller_state = "RUNNING"

    @staticmethod
    def get_task():
        # If completed, else keep the state
        RpcController.controller_state = "COMPLETED"

    @staticmethod
    def kill_task():
        RpcController.controller_state = "COMPLETED"
