import numpy as np
from counter import Counter
from utils.shapes import Box, Line

# The structure of the T-Intersection is as follows
#           |   |
#           | T |
# ----------     -----------
#        A          B
# --------------------------
# T: Only turning traffics
# A & B: One turning traffic and one straight traffic


class CrossCounter(Counter):
    def __init__(self, fps, A: Line, B: Line, T: Line):
        self.detector = detector
        self.fps = fps
        self.A, self.B, self.T = A, B, T

        self.occurence_stack = []
        self.realized_flow = {
            "A": {
                "Left": 0,
                "Straight": 0
            },
            "B": {
                "Right": 0,
                "Straight": 0
            },
            "T": {
                "Left": 0,
                "Right": 0,
            }
        }

    def getFlow(self):
        output_flow = copy.deepcopy(self.realized_flow)
        for i in range(0, len(self.occurence_stack), 2):
            self.increment_flow(
                output_flow,
                self.occurence_stack[i][1],
                self.occurence_stack[i + 1][1]
            )
        return output_flow

    def update(self, id, vehicle: Box):
        detected_line = None
        if self.hover(self.A, vehicle):
            detected_line = "A"
        if self.hover(self.B, vehicle):
            detected_line = "B"
        if self.hover(self.T, vehicle):
            detected_line = "T"
        
        if not detected_line is None:
            self.occurence_stack.append((id, detected_line))

        while self.update_realized_flow():
            pass

    def update_realized_flow():
        for src in range(0, len(self.occurence_stack)):
            for dst in range(src + 1, len(self.occurence_stack)):
                if self.occurence_stack[src][0] == self.occurence_stack[dst][0]:
                    self.increment_flow(
                        self.realized_flow,
                        self.occurence_stack[src][1],
                        self.occurence_stack[dst][1]
                    )
                    self.occurence_stack.pop(src)
                    self.occurence_stack.pop(dst)
                    return True
        return False
    
    def increment_flow(flow, origin, dest):
        direction = 'Straight' if (origin, dest) in [
            ('A', 'B'), ('B', 'A')
        ] else None
        direction = 'Left' if (origin, dest) in [
            ('A', 'T'), ('T', 'B')
        ] else None
        direction = 'Right' if (origin, dest) in [
            ('T', 'A'), ('B', 'T')
        ] else None
        flow[origin][direction] += 1