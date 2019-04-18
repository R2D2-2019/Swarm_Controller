from command_node import CommandNode
import json

# The controller for the commandline interface
class CLIController:
    # Files given have to be JSON files.
    def __init__(self, tmp_command_file_list=None):
        self.root_node = CommandNode("ROOT")
        self.global_commands = {
            "exit": ["EXIT", "LEAVE", "QUIT", "Q"],
            "help": ["HELP"],
            "back": ["BACK", "RETURN"],
            "root": ["ROOT"]
        }
        self.module_commands = []
        self.command_file_list = tmp_command_file_list
        self.load_tree()

    # Loads all files
    def load_tree(self):
        for file in self.command_file_list:
            self.load_commands(file)

    # Loads a single file into commands
    def load_commands(self, tmp_file):
        with open(tmp_file, "r") as json_file:
            data = json.load(json_file)
            try:
                # Check how far the path already exists
                #   - If the command has some of the preserved keywords, the program exits.
                #   - Any missing links in the tree will be added
                for command in data["commands"]:
                    for command_type in self.global_commands:
                        if command["target"].upper() in self.global_commands[command_type]:
                            exit("Used keyword {} as target. Using keywords is prohibited!".format(command["target"]))
                    current_node = self.root_node
                    # Per path checking if it has a child
                    for path_piece in command["path"].split(" "):
                        for command_type in self.global_commands:
                            if path_piece.upper() in self.global_commands[command_type]:
                                exit("Used keyword {} as target. Using keywords is prohibited!".format(command["target"]))
                        # If the current path info already exists, traverse the tree
                        if current_node.has_child(path_piece):
                            current_node = current_node.get_child(path_piece)
                        # Else, add the missing link
                        else:
                            new_node = CommandNode(path_piece, current_node)
                            new_node.set_parent(current_node)
                            current_node.add_child(new_node)
                            current_node = new_node
                    # After all the missing links in the tree are made, add the command
                    target_node = CommandNode(command["target"], tmp_parameter_list=command["parameters"], tmp_command_info=command["info"])
                    target_node.set_parent(current_node)
                    current_node.add_child(target_node)
            except KeyError as error:
                print("Key {} was not found".format(error))

    # Joins given list and appends a ':'
    # Expects a list
    @staticmethod
    def make_path_string(tmp_path_list):
        return ' / '.join(tmp_path_list) + ":"

    # Prints the info of the node.
    # If the node has no parameters, it will print its children.
    @staticmethod
    def print_help(node):
        print(node.name + ":")
        print("Info: " + node.command_info)
        if len(node.parameter_list) > 0:
            print("Parameters: (" + (", ".join(node.parameter_list)) + ")")
        else:
            # Lists children
            if node.get_child_amount() > 0:
                print("Children: {}".format(", ".join(node.children)))
            else:
                print("This function requires no parameters")

    # Starts an infinite loop (until exit command is called) which polls for input
    def start_cli(self):
        current_node = self.root_node
        while True:
            path_list = current_node.get_all_parents()
            path_string = self.make_path_string(path_list)
            user_command = input(path_string)
            user_command_list = user_command.split(" ")
            for user_word in user_command_list:

                # Step 1: Check for globals
                is_global = False
                for command_type in self.global_commands:
                    if user_word.upper() in self.global_commands[command_type]:
                        is_global = True
                        if command_type == "exit":
                            exit()
                        elif command_type == "help":
                            self.print_help(current_node)
                        elif command_type == "back":
                            current_node = current_node.parent
                        elif command_type == "root":
                            current_node = self.root_node

                # Step 2: Check for children
                if not is_global:
                    if current_node.has_child(user_word.upper()):
                        current_node = current_node.get_child(user_word.upper())
                    else:
                        print("Command {} not found, possible commands: {}".format(user_word, ", ".join(current_node.children)))
                        break
