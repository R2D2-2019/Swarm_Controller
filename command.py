class command_node:
    def __init__(self, tmp_name, tmp_parent = None):
        assert(type(tmp_name) is not None)
        self.name = tmp_name.upper()
        self.children = dict()
        self.parent = tmp_parent
        self.function = None

    def add(self, tmp_child):
        self.children[tmp_child.name.upper()] = tmp_child

    def get_parents(self):
        if self.parent is None:
            return [self.name]
        else:
            return self.parent.get_parents() + [self.name]

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

    def do_function(self, *args):
        if type(self.function) == str:
            print(self.function)
        elif callable(self.function):
            self.function(*args)
        else:
            print("{} has no function".format(self.name))
            print(self.function)

    def set_function(self, tmp_function):
        self.function = tmp_function
