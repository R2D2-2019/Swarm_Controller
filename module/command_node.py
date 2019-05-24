from common.common import AutoNumber


class NodeType(AutoNumber):
    NONE = ()
    ROOT = ()
    CATEGORY = ()
    COMMAND = ()


# Represents a node in a tree, this node knows its parent
class Node(dict):
    def __init__(
        self,
        name,
        node_type=NodeType.NONE,
        parent=None,
        parameter_list=None,
        command_info="Currently none available",
    ):

        if parameter_list is None:
            parameter_list = list()

        self.name = name.upper()
        self.parent = parent
        self.parameter_list = parameter_list
        self.command_info = command_info
        self.type = node_type

    """
    Gets all names of nodes in this branch in a list, ordered as root first
    """

    def get_branch_names(self) -> list:
        if self.parent is None:
            return [self.name]
        else:
            return self.parent.get_branch_names() + [self.name]

    """
    Sets the parent to given parent
    """

    def set_parent(self, parent) -> None:
        self.parent = parent
