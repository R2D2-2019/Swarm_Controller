class command_node:
    def __init__(self, tmp_name, tmp_parent = None):
        assert(type(tmp_name) is not None)
        self.name = tmp_name.upper()
        self.children = dict()
        self.parent = tmp_parent

    def add_child(self, tmp_child):
        self.children[tmp_child.name.upper()] = tmp_child

    def get_parent(self):
        if self.parent is None:
            return [self.name]
        else:
            return self.parent.get_parents() + [self.name]

    def set_parent(self, tmp_parent):
        self.parent = tmp_parent

    def show_children(self):
        if( len(self.children) > 0):
            for child_key in self.children:
                print(self.children[child_key].name)

    def has_child(self, key):
        return key.upper() in self.children

    def get_child_amount(self):
        return len(self.children)

    def get_child(self, key):
        if key.upper() in self.children:
            return self.children[key.upper()]
        else:
            return None
