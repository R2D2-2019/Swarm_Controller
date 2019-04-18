# Represents a node in a tree, this node knows its parent
class CommandNode:
    def __init__(self,
                 tmp_name,
                 tmp_parent=None,
                 tmp_parameter_list=list(),
                 tmp_command_info="Currently none available"):

        assert (type(tmp_name) is not None)
        self.name = tmp_name.upper()
        self.children = dict()
        self.parent = tmp_parent
        self.parameter_list = tmp_parameter_list
        self.command_info = tmp_command_info

    # This function adds a child, or overrides it when it exists
    def add_child(self, tmp_child):
        self.children[tmp_child.name.upper()] = tmp_child

    # Gets all parents in a list, ordered as root first
    def get_all_parents(self):
        if self.parent is None:
            return [self.name]
        else:
            return self.parent.get_all_parents() + [self.name]

    # Sets the parent to given parent
    def set_parent(self, tmp_parent):
        self.parent = tmp_parent

    # Displays the children of this node
    def show_children(self):
        if len(self.children) > 0:
            for child_key in self.children:
                print(self.children[child_key].name)

    # Returns true if this node has give key (name) as a direct child, else returns false
    def has_child(self, key):
        return key.upper() in self.children

    # Gets the amount of children this node has
    def get_child_amount(self):
        return len(self.children)

    # Returns a child at the given key. Returns None if no key matches.
    def get_child(self, key):
        if key.upper() in self.children:
            return self.children[key.upper()]
        else:
            return None
