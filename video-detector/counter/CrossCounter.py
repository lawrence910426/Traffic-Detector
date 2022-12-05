import numpy as np
from counter import Counter
from utils.shapes import Box, Line

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
    def __init__(self, fps, A: Line, B: Line, T: Line):
        self.detector = detector
        self.fps = fps

        self.state = {}
        self.flow = {
            "Forward": 0,
            "Reverse": 0
        }

    def getFlow(self):
        pass

    def update(self, id, vehicle: Box):
        # self.hover(A, vehicle):
        pass
