from client.comm import BaseComm
from common.frames import FrameUiCommand
import inspect


def cast_and_send_ui_frame(comm: BaseComm, frame_name: str, params: list, destination: str) -> None:
    """
    Creates and sends a FrameUiCommand with parameters frame_name, params and destination.
    """
    frame = FrameUiCommand()
    frame.set_data(frame_name, " ".join(str(param) for param in params), destination)
    comm.send(frame)


def get_frames_with_description(mod) -> list:
    """
    Gets all the frames from the 'mod' module which have a DESCRIPTION variable which is not empty.
    """
    # Get all classes from only mod
    frames = inspect.getmembers(
        mod, lambda member: inspect.isclass(member) and member.__module__ == mod.__name__
    )

    return [frame for frame in frames if frame[1].DESCRIPTION]
