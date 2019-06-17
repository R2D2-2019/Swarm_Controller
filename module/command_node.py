from client.comm import BaseComm
from common.frames import FrameUiCommand
from typing import Callable


class Node(dict):
    def __init__(self, name: str, node_info: str ="Currently none available"):
        """
        A dictionary with a name and node_info variable.

        @param name is the name of the node
        @param node_info is the info of the node that will be displayed when typing help
        """
        self.name = name
        self.node_info = node_info


class Command(Node):
    def __init__(self, name: str, node_info: str = "Currently none available"):
        """
        A Node which can send a frame (using the send method) according to it's required parameters.

        @param name is the name of the node
        @param node_info is the info of the node that will be displayed when typing help
        """
        super().__init__(name, node_info=node_info)

    def send(self, comm: BaseComm, params: list, destination: str) -> None:
        """
        Creates and sends a FrameUiCommand with parameters frame_name, params and destination.
        
        
        

        @param comm must be a BaseComm from the client.comm module (python-bus)
        @param params is the list of parameters to be passed in to the frame
        @param destination is the name of the target (robot / swarm)
        """
        frame = FrameUiCommand()
        frame.set_data(self.name, " ".join(str(param) for param in params), destination)
        comm.send(frame)


class GlobalCommand(Node):
    def __init__(self, name: str, func: Callable, node_info: str = "Currently none available"):
        """
        A node which can execute its stored function (func) with given parameters using the execute method.

        @param name is the name of the node
        @param func is the function that will be executed when using the execute function
        @param node_info is the info of the node that will be displayed when typing help
        """
        super().__init__(name, node_info=node_info)
        self.func = func

    def execute(self, params: list):
        """
        Executes self.func using the given parameters.

        @param params are all the parameters that will be sent with func
        """
        return self.func(params)
