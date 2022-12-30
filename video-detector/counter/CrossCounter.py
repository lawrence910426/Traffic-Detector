import numpy as np
from utils.shapes import Box, Line
from .StackCounter import StackCounter

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

class CrossCounter(StackCounter):
    def __init__(self, fps, logger, A: Line, B: Line, X: Line, Y: Line):
        super().__init__(logger)
        
        self.fps = fps
        self.A, self.B, self.X, self.Y = A, B, X, Y
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

    def update(self, id, vehicle: Box):
        detected_line = None
        if self.hover(self.A, vehicle):
            detected_line = "A"
        if self.hover(self.B, vehicle):
            detected_line = "B"
        if self.hover(self.X, vehicle):
            detected_line = "X"
        if self.hover(self.Y, vehicle):
            detected_line = "Y"
        
        if not detected_line is None:
            self.occurence_stack.append((id, detected_line))

        while self.update_realized_flow():
            pass
    
    def increment_flow(self, flow, origin, dest):
        direction = None
        direction = 'Straight' if (origin, dest) in [
            ('X', 'Y'), ('Y', 'X'), ('A', 'B'), ('B', 'A')
        ] else direction
        direction = 'Left' if (origin, dest) in [
            ('A', 'X'), ('X', 'B'), ('B', 'Y'), ('Y', 'A')
        ] else direction
        direction = 'Right' if (origin, dest) in [
            ('X', 'A'), ('B', 'X'), ('Y', 'B'), ('A', 'Y')
        ] else direction
        
        if direction is None:
            return False
        else:
            flow[origin][direction] += 1
            return True