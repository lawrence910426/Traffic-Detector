import numpy as np
import copy
from utils.shapes import Box, Line
from .Counter import Counter

class StraightCounter(Counter):
    def __init__(self, logger, x: Line, y: Line):
        super().__init__(logger)
        self.X, self.Y = x, y
        
        self.occurence_stack = {}
        self.vehicle_status = {}

        self.lone_directions = { "X": {}, "Y": {}, "Q": {} }    # { direction: { id: idx_frame } }
        self.lone_timeline = { }                                # { idx_frame: [ (direction, id) ] }
        
        self.flow = {
            "Forward": set(),
            "Reverse": set()
        }
        self.life_time = 300

    def calibrate_lone_set(self):
        calibrate = { "Forward": 0, "Reverse": 0 }
        events = sorted(self.lone_timeline.keys(), reverse=True)
        timeline = copy.deepcopy(self.lone_timeline)

        # Greedily match the events with nearest time first.
        while True:
            try:
                for latest, lid in timeline[events[0]]:
                    complement = set(['X', 'Y', 'Q']) - set([latest])
                    for i in range(1, len(events)):
                        for match, mid in timeline[events[i]]:
                            if match in complement:
                                # Add to flow
                                calibrate["Forward" if latest == 'X' else "Reverse"] += 1
                                
                                # Remove the matched events
                                timeline[events[0]].remove((latest, lid))
                                if len(timeline[events[0]]) == 0:
                                    timeline.pop(events[0])
                                    events.remove(events[0])
                                timeline[events[i]].remove((match, mid))
                                if len(timeline[events[i]]) == 0:
                                    timeline.pop(events[i])
                                    events.remove(events[i])

                                # Restart the loop
                                raise
                
                # No more possible matches
                return calibrate
            except:
                continue

    def getFlow(self):
        calibration = self.calibrate_lone_set()
        return {
            "Forward": len(self.flow["Forward"]) + calibration["Forward"],
            "Reverse": len(self.flow["Reverse"]) + calibration["Reverse"]
        }

    def update(self, id, idx_frame, vehicle: Box):
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
        
        # Handles lone_set
        direction = self.occurence_stack[id][0]
        if len(self.occurence_stack[id]) == 1:
            self.lone_directions[direction][id] = idx_frame

            # Add to lone_timeline
            if not idx_frame in self.lone_timeline:
                self.lone_timeline[idx_frame] = []
            self.lone_timeline[idx_frame].append((direction, id))
        else:
            # Remove from lone_timeline if exists
            initial_frame = self.lone_directions[direction][id]
            if initial_frame in self.lone_timeline:
                if (direction, id) in self.lone_timeline[initial_frame]:
                    self.lone_timeline[initial_frame].remove((direction, id))
                
                # Drop empty list
                if len(self.lone_timeline[initial_frame]) == 0:
                    self.lone_timeline.pop(initial_frame)

            # Remove from lone_set if exists
            self.lone_directions[direction].pop(id, None)

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

        
                