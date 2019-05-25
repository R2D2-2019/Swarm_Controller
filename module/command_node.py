from client.comm import BaseComm
from common.frames import FrameUiCommand


class Node(dict):
    def __init__(self, name, node_info="Currently none available"):
        self.name = name
        self.node_info = node_info


class Command(Node):
    def __init__(self, name: str, node_info: str = "Currently none available"):
        super().__init__(name, node_info=node_info)

    def send(self, comm: BaseComm, params: list, destination: str) -> None:
        """
        Creates and sends a FrameUiCommand with parameters frame_name, params and destination.
        """
        frame = FrameUiCommand()
        frame.set_data(self.name, " ".join(str(param) for param in params), destination)
        comm.send(frame)


class GlobalCommand(Node):
    def __init__(self, name: str, func, node_info: str = "Currently none available"):
        super().__init__(name, node_info=node_info)
        self.func = func

    def execute(self, params: list):
        return self.func(params)
