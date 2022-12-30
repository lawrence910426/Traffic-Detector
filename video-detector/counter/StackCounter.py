import copy
from .Counter import Counter

# This implements the stack matching algorithm
# for traffic flow detection.
# Erich was here
class StackCounter(Counter):
    def __init__(self, logger):
        super().__init__(logger)
        self.occurence_stack = []
        self.vehicle_status = {}

    def append_detection(self, id, line):
        self.logger.info(
            "Detection status " + str(id)  + " " + str(line)
        )

        if (not id in self.vehicle_status) or (self.vehicle_status[id] != line):
            self.vehicle_status[id] = line
            self.occurence_stack.append((id, line))

    def getFlow(self):
        flow = copy.deepcopy(self.realized_flow)
        stack = copy.deepcopy(self.occurence_stack)

        while self.fix_flow(flow, stack):
            pass
        
        self.logger.info(
            "Stack status " +
            str(stack) + " " + str(self.occurence_stack)
        )
        return flow

    def fix_flow(self, flow, stack):
        for src in range(0, len(stack)):
            for dst in range(src + 1, len(stack)):
                if self.increment_flow(
                    flow, stack[src][1], stack[dst][1]
                ):
                    # Since src has been popped, the index 
                    # of dst is shifted forward by 1
                    stack.pop(src)
                    stack.pop(dst - 1)
                    return True
        return False

    def update_realized_flow(self):
        for src in range(0, len(self.occurence_stack)):
            for dst in range(src + 1, len(self.occurence_stack)):
                if self.occurence_stack[src][0] == self.occurence_stack[dst][0]:
                    self.increment_flow(
                        self.realized_flow,
                        self.occurence_stack[src][1],
                        self.occurence_stack[dst][1]
                    )
                    # Since src has been popped, the index 
                    # of dst is shifted forward by 1
                    self.occurence_stack.pop(src)
                    self.occurence_stack.pop(dst - 1)
                    return True
        return False