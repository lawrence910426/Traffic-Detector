import numpy as np
from utils.shapes import Box, Line
from .StackCounter import StackCounter

# The structure of the T-Intersection is as follows
#           |   |
#           | T |
# ----------     -----------
#        A          B
# --------------------------
# T: Only turning traffics
# A & B: One turning traffic and one straight traffic


class TCounter(StackCounter):
    def __init__(self, logger, A: Line, B: Line, T: Line):
        super().__init__(logger)

        self.A, self.B, self.T = A, B, T
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

    def update(self, id, idx_frame, vehicle: Box):
        detected_line = None
        if self.hover(self.A, vehicle):
            detected_line = "A"
        if self.hover(self.B, vehicle):
            detected_line = "B"
        if self.hover(self.T, vehicle):
            detected_line = "T"
        
        if not detected_line is None:
            self.append_detection(id, detected_line)

        while self.update_realized_flow():
            pass

    def increment_flow(self, flow, origin, dest):
        direction = None
        direction = 'Straight' if (origin, dest) in [
            ('A', 'B'), ('B', 'A')
        ] else direction
        direction = 'Left' if (origin, dest) in [
            ('A', 'T'), ('T', 'B')
        ] else direction
        direction = 'Right' if (origin, dest) in [
            ('T', 'A'), ('B', 'T')
        ] else direction
        
        if direction is None:
            return False
        else:
            flow[origin][direction] += 1
            return True