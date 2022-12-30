class Box:
    def __init__(self, x1, y1, x2, y2):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

class Line:
    def __init__(self, x1, y1, x2, y2, swapXY=False):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        if swapXY:
            self.x1, self.y1, self.x2, self.y2 = y1, x1, y2, x2
        else:
            self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2