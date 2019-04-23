# Represents a node in a tree, this node knows its parent
class CommandNode:
    def __init__(self,
                 name,
                 parent=None,
                 parameter_list=None,
                 command_info="Currently none available"):

        if parameter_list is None:
            parameter_list = list()

        self.name = name.upper()
        self.children = dict()
        self.parent = parent
        self.parameter_list = parameter_list
        self.command_info = command_info

    """
    This function adds a child, or overrides it when it exists
    """
    def add_child(self, child):
        self.children[child.name.upper()] = child

    """
    Gets all names of nodes in this branch in a list, ordered as root first
    """
    def get_branch_names(self):
        if self.parent is None:
            return [self.name]
        else:
            return self.parent.get_branch_names() + [self.name]

    """
    Sets the parent to given parent
    """
    def set_parent(self, parent):
        self.parent = parent

    """
    Displays the children of this node
    """
    def show_children(self):
        if self.children:
            for child_key in self.children:
                print(self.children[child_key].name)

    """ 
    Returns true if this node has give key (name) as a direct child, else returns false
    """
    def has_child(self, key):
        return key.upper() in self.children

    """
    Gets the amount of children this node has
    """
    def get_child_amount(self):
        return len(self.children)

    """
    Returns a child at the given key. Returns None if no key matches.
    """
    def get_child(self, key):
        if key.upper() in self.children:
            return self.children[key.upper()]
        else:
            return None
