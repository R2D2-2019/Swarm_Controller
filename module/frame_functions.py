from client.comm import BaseComm
from common.frames import FrameUiCommand
import inspect


def get_frames_with_description(mod) -> list:
    """
    Gets all the frames from the 'mod' module which have a DESCRIPTION variable which is not empty.
    
    @param mod is the class which description will be read
    """
    # Get all classes from only mod
    frames = inspect.getmembers(
        mod,
        lambda member: inspect.isclass(member) and member.__module__ == mod.__name__,
    )

    return [frame for frame in frames if frame[1].DESCRIPTION]
