import numpy as np
from counter import Counter
from utils.shapes import Box, Line
import copy

# The structure of the Cross Intersection is as follows
#           |   |
#           | X |
# ----------     -----------
#       A            B
# ----------     -----------
#           | Y |
#           |   |
# 
# (A, B) and (X, Y) are perpendicular.

class CrossCounter(Counter):
    def __init__(self, fps, A: Line, B: Line, X: Line, Y: Line):
        self.detector = detector
        self.fps = fps

        self.occurence_stack = []
        self.realized_flow = {
            "A": {
                "Left": 0,
                "Right": 0,
                "Straight": 0
            },
            "B": {
                "Left": 0,
                "Right": 0,
                "Straight": 0
            },
            "X": {
                "Left": 0,
                "Right": 0,
                "Straight": 0
            },
            "Y": {
                "Left": 0,
                "Right": 0,
                "Straight": 0
            },
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
        if self.hover(A, vehicle):
            detected_line = "A"
        if self.hover(B, vehicle):
            detected_line = "B"
        if self.hover(X, vehicle):
            detected_line = "X"
        if self.hover(Y, vehicle):
            detected_line = "Y"
        
        if not detected_line is None:
            self.occurence_stack.append((id, detected_line))

        while self.update_realized_flow():
            pass

    def update_realized_flow():
        for src in range(0, len(self.occurence_stack))
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
            ('X', 'Y'), ('Y', 'X'), ('A', 'B'), ('B', 'A')
        ] else None
        direction = 'Left' if (origin, dest) in [
            ('A', 'X'), ('X', 'B'), ('B', 'Y'), ('Y', 'A')
        ] else None
        direction = 'Right' if (origin, dest) in [
            ('X', 'A'), ('B', 'X'), ('Y', 'B'), ('A', 'Y')
        ] else None
        flow[origin][direction] += 1