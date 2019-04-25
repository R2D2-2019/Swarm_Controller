import json
from command_node import CommandNode


class CLIController:
    """
    Filenames given have to be JSON files.
    """
    def __init__(self, command_file_list=None):
        self.root_node = CommandNode("ROOT")

        # These function as preserved keywords, do not use these names in commands

        self.global_commands = {
            "exit": ["EXIT", "LEAVE", "QUIT", "Q"],
            "help": ["HELP"],
            "back": ["BACK", "RETURN"],
            "root": ["ROOT"]
        }
        self.module_commands = []
        self.command_file_list = command_file_list
        self.load_tree()

    """
    Loads all files into command structure
    """
    def load_tree(self):
        for file in self.command_file_list:
            self.load_commands(file)

    """
    Loads a single JSON file into command structure
    """
    def load_commands(self, file):
        with open(file, "r") as json_file:
            data = json.load(json_file)
            try:

                # Check how far the path already exists
                # - If the command has some of the preserved keywords, the program exits.
                # - Any missing links in the tree will be added

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
                        # Else, add the missing link

                        if path_piece.upper() in current_node:
                            current_node = current_node[path_piece.upper()]
                        else:
                            new_node = CommandNode(path_piece, current_node)
                            new_node.set_parent(current_node)
                            current_node[new_node.name] = new_node
                            current_node = new_node

                    # After all the missing links in the tree are made, add the command
                    target_node = CommandNode(
                        command["target"],
                        parameter_list=command["parameters"],
                        command_info=command["info"]
                    )
                    target_node.set_parent(current_node)
                    current_node[target_node.name] = target_node
            except KeyError as error:
                print("Key {} was not found".format(error))

    """
    Joins given list and appends a ':'
    Expects a list
    """
    @staticmethod
    def make_path_string(path_list):
        return ' / '.join(path_list) + ":"

    """
    Prints the info and any children or parameters of the node.
    """
    @staticmethod
    def print_help(node):
        print(node.name + ":")
        print("\tInfo: " + node.command_info)
        if node.parameter_list:
            print("\tParameters: (" + (", ".join(node.parameter_list)) + ")")
        elif len(node) > 0:
            print("\tChildren: {}".format(", ".join(node[n].name.lower() for n in node.keys())))
        else:
            print("\tThis function requires no parameters and has no children")

    """
    Starts an infinite loop (until exit command is called) which polls for input
    """
    def start_cli(self):
        current_node = self.root_node
        while True:
            path_list = current_node.get_branch_names()
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
                    if user_word.upper() in current_node:
                        current_node = current_node[user_word.upper()]

                    elif len(current_node.parameter_list) > 0:
                        print("Command called with {} parameters: {}".format(
                            len(user_command_list[user_command_list.index(user_word):]),
                            "(" + ",".join(user_command_list[user_command_list.index(user_word):]) + ")"
                        ))
                        break

                    else:
                        print("Command {} not found, possible commands: {}".format(user_word, ", ".join(current_node.children)))
                        break
