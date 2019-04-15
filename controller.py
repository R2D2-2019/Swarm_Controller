from command import command_node
import json

class controller:
    def __init__(self, tmp_command_file_list = None):
        self.root_node = command_node("ROOT")
        self.global_commands = []
        self.module_commands = []
        self.command_file_list = tmp_command_file_list
        self.load_tree()
    
    def load_tree(self):
        for file in self.command_file_list:
            self.load_commands(file)
    
    def load_commands(self, tmp_file):
        with open(tmp_file, "r") as json_file:
            data = json.load(json_file)
            for command in data["commands"]:
                current_node = self.root_node
                for path_piece in command["path"].split(" "):
                    if current_node.has_child(path_piece):
                        current_node = current_node.get_child(path_piece)
                    else:
                        new_node = command_node(path_piece, current_node)
                        new_node.set_parent(current_node)
                        current_node.add_child(new_node)
                        current_node = new_node
                target_node = command_node(command["target"])
                target_node.set_parent(current_node)
                current_node.add_child(target_node)

