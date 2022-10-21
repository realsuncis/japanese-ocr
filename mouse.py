import win32api
from position import Position

class MouseManager:

    def __init__(self):
        self._lastPosition = Position(0, 0)

    def getPosition(self):
        x, y = win32api.GetCursorPos()
        return Position(x, y)

    def positionChanged(self):
        x, y = win32api.GetCursorPos()
        if self._lastPosition.x != x or self._lastPosition.y != y:
            return True
        else:
            return False

    def update(self):
        x, y = win32api.GetCursorPos()
        self._lastPosition = Position(x, y)