import numpy as np
from utils.shapes import Box, Line
from .Counter import Counter

class StraightCounter(Counter):
    def __init__(self, logger, x: Line, y: Line, z: Line):
        super().__init__(logger)
        self.X, self.Y, self.Z = x, y, z
        
        self.occurence_stack = {}
        self.vehicle_status = {}

        self.flow = {
            "Forward": set(),
            "Reverse": set()
        }

    def getFlow(self):
        return {
            "Forward": len(self.flow["Forward"]),
            "Reverse": len(self.flow["Reverse"])
        }

    def update(self, id, vehicle: Box):
        if not (id in self.occurence_stack):
            self.occurence_stack[id] = []
            self.vehicle_status[id] = None
        
        detected_line = None
        if self.hover(self.X, vehicle):
            detected_line = "X"
        if self.hover(self.Y, vehicle):
            detected_line = "Y"
        if self.hover(self.Z, vehicle):
            detected_line = "Z"

        if not detected_line is None and self.vehicle_status[id] != detected_line:
            self.occurence_stack[id].append(detected_line)
            self.vehicle_status[id] = detected_line
        
        # There is only 1 vehicle in the stack
        if len(self.occurence_stack[id]) < 2:
            return
        
        direction = None
        direction = 'Forward' if (self.occurence_stack[id][0], self.occurence_stack[id][1]) in [
            ('X', 'Y'), ('Y', 'Z')
        ] else direction
        direction = 'Reverse' if (self.occurence_stack[id][0], self.occurence_stack[id][1]) in [
            ('Z', 'Y'), ('Y', 'X')
        ] else direction

        # Hop from (X to Z) or (Z to X)
        if direction is None:
            return 
        
        # Must be invalid, since the below cases are not valid and (X, Y, Z, Z) is not possible
        # (X, Y, Z, Y), (X, Y, Z, X)
        # (Z, Y, X, Y), (Z, Y, X, Z)
        if len(self.occurence_stack[id]) > 3:
            self.flow[direction].remove(id)
            return

        # (X, Y, Z) and (Z, Y, X) is the only allowed case
        if direction == 'Forward' and self.occurence_stack[id][2] != 'Z':
            self.flow[direction].remove(id)
            return
        if direction == 'Reverse' and self.occurence_stack[id][2] != 'X':
            self.flow[direction].remove(id)
            return
        
        # `id` might be added twice. First time when there is only 2 element in the stack.
        # Second time when there is 3 element in the stack.
        self.flow[direction].add(id)

