import numpy as np

NaN = float('nan')

class SwingingDoor:
    def __init__(self, tolerance):
        self.tolerance = tolerance
        self.curx, self.cury = None, NaN
        self.startx, self.starty = None, NaN
        self.data = []

    def run(self, x, y):
        p = self.checkPoint(x, y)
        if p is not None:
            self.start(*p)
            self.save(*p)

    def start(self, x, y):
        if y == y:
            self.startx, self.starty = x, y
            if self.curx > x:
                dx = self.curx - x
                dy = self.cury - y
                self.fu = (dy - self.tolerance) / dx
                self.fl = (dy + self.tolerance) / dx
            else:
                self.fl, self.fu = 1000000, -1000000
        else:
            self.curx = None

    def checkSlopes(self, x, y):
        dx = x - self.startx
        dy = y - self.starty
        fu = (dy - self.tolerance) / dx
        fl = (dy + self.tolerance) / dx

        if fu > self.fu:
            self.fu = fu
        if fl < self.fl:
            self.fl = fl
        if self.fu > self.fl:
            return self.curx, self.cury

    def checkPoint(self, x, y):
        if y == y:
            if self.curx is None:
                self.curx, self.cury = x, y
                return x, y

            if self.curx >= x:
                return

            r = self.checkSlopes(x, y)
            self.curx, self.cury = x, y
            return r
        elif self.curx is not None:
            if self.cury == self.cury:
                self.save(self.curx, self.cury)
                self.curx, self.cury = x, y
            else:
                self.save(self.curx, self.cury)
                self.curx = None

    def save(self, x, y):
        self.data.append((x, y))
