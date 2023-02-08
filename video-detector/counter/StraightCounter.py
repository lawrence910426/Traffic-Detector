import numpy as np
from utils.shapes import Box, Line
from .Counter import Counter

class StraightCounter(Counter):
    def __init__(self, logger, x: Line, y: Line):
        super().__init__(logger)
        self.X, self.Y = x, y
        
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
        
        detected_line = []
        if self.hover(self.X, vehicle):
            detected_line.append("X")
        if self.hover(self.Y, vehicle):
            detected_line.append("Y")

        detected_symbol = None
        detected_symbol = detected_line[0] if len(detected_line) == 1 else detected_symbol
        detected_symbol = 'Q' if len(detected_line) == 2 else detected_symbol

        if self.vehicle_status[id] != detected_symbol:
            self.occurence_stack[id].append(detected_symbol)
            self.vehicle_status[id] = detected_symbol

        # There are 2 occurences in the stack. 
        if len(self.occurence_stack[id]) == 2:
            direction = None
            direction = 'Forward' if (self.occurence_stack[id][0], self.occurence_stack[id][1]) in [
                ('X', 'Y'), ('Q', 'Y'), ('X', 'Q')
            ] else direction
            direction = 'Reverse' if (self.occurence_stack[id][0], self.occurence_stack[id][1]) in [
                ('Y', 'X'), ('Q', 'X'), ('Y', 'Q')
            ] else direction

            if not direction is None:
                self.flow[direction].add(id)

        # There are 3 occurences in the stack. Must be (X, Q, Y) or (Y, Q, X)
        if len(self.occurence_stack[id]) == 3:
            direction = None
            direction = 'Forward' if (self.occurence_stack[id][0], self.occurence_stack[id][2]) in [
                ('X', 'Y')
            ] else direction
            direction = 'Reverse' if (self.occurence_stack[id][0], self.occurence_stack[id][2]) in [
                ('Y', 'X')
            ] else direction

            if not direction is None:
                self.flow[direction].add(id)
                