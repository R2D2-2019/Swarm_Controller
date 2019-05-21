# these frames are used for testing in other test files, not using the python bus frames.py because that one can change at any moment

from common.frames import Frame
from common.frame_enum import FrameType
import struct


class FrameButtonState(Frame):
    MEMBERS = ['pressed']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameButtonState, self).__init__()
        self.type = FrameType.BUTTON_STATE
        self.format = '?'
        self.length = 1

    def set_data(self, pressed: bool):
        self.data = struct.pack(self.format, pressed)


class FrameActivityLedState(Frame):
    MEMBERS = ['state']
    DESCRIPTION = "Packet containing the state of\nan activity led.\n"

    def __init__(self):
        super(FrameActivityLedState, self).__init__()
        self.type = FrameType.ACTIVITY_LED_STATE
        self.format = '?'
        self.length = 1

    def set_data(self, state: bool):
        self.data = struct.pack(self.format, state)

class FrameDistance(Frame):
    MEMBERS = ['mm']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameDistance, self).__init__()
        self.type = FrameType.DISTANCE
        self.format = 'H'
        self.length = 2

    def set_data(self, mm: int):
        self.data = struct.pack(self.format, mm)

class FrameDisplayFilledRectangle(Frame):
    MEMBERS = ['x', 'y', 'width', 'height', 'red', 'green', 'blue']
    DESCRIPTION = "Struct to set a rectangle on a display. This fills a\nrectangle with the color specified.\n\nCurrently we can't fill the bigger screens. When the\nextended frames are here the position and width/height\nwill change to a uint16_t to support the bigger screens.\n\nDisplay wiki:\nhttps://github.com/R2D2-2019/R2D2-2019/wiki/Display\n"

    def __init__(self):
        super(FrameDisplayFilledRectangle, self).__init__()
        self.type = FrameType.DISPLAY_FILLED_RECTANGLE
        self.format = 'BBBBBBB'
        self.length = 7

    def set_data(self, x: int, y: int, width: int, height: int, red: int, green: int, blue: int):
        self.data = struct.pack(self.format, x, y, width, height, red, green, blue)