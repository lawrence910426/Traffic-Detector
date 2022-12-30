import numpy as np
from utils.shapes import Box, Line

class Counter:
    def __init__(self, logger):
        self.logger = logger

    def getFlow(self):
        return None

    def hover(self, detector: Line, vehicle: Box):
        seg, rect = detector, vehicle
        self.logger.info(
            "Hover params: seg = {} {} {} {}, box = {} {} {} {}".format(
                seg.x1, seg.x2, seg.y1, seg.y2,
                rect.x1, rect.x2, rect.y1, rect.y2,
            )
        )

        # Either point in the box
        inside = lambda x, y: rect.x1 <= x and x <= rect.x2 and rect.y1 <= y and y <= rect.y2
        if inside(seg.x1, seg.y1) or inside(seg.x2, seg.y2):
            return True
        
        # The line penetrates the box
        if seg.x2 != seg.x1:
            formula = lambda x: (seg.y2 - seg.y1) / (seg.x2 - seg.x1) * (x - seg.x1) + seg.y1
            if min(seg.x1, seg.x2) <= rect.x1 <= max(seg.x1, seg.x2) and rect.y1 <= formula(rect.x1) <= rect.y2:
                return True
            if min(seg.x1, seg.x2) <= rect.x2 <= max(seg.x1, seg.x2) and rect.y1 <= formula(rect.x2) <= rect.y2:
                return True

        if seg.y2 != seg.y1:
            formula = lambda y: (seg.x2 - seg.x1) / (seg.y2 - seg.y1) * (y - seg.y1) + seg.x1
            if min(seg.y1, seg.y2) <= rect.y1 <= max(seg.y1, seg.y2) and rect.x1 <= formula(rect.y1) <= rect.x2:
                return True
            if min(seg.y1, seg.y2) <= rect.y2 <= max(seg.y1, seg.y2) and rect.x1 <= formula(rect.y2) <= rect.x2:
                return True
        
        return False
