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

class TCounter(Counter):
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
