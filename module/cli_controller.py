import json
import threading
import queue

from client.comm import BaseComm

from module.command_node import CommandNode


class CLIController:
    """
    Filenames given have to be JSON files.
    """
    def __init__(self, comm:BaseComm, command_file_list=None):
        self.comm = comm
        self.root_node = CommandNode("ROOT")

        self.input_queue = queue.Queue()
        self.input_thread = threading.Thread()

        # These function as preserved keywords, do not use these names in commands

        self.global_commands = {
            "exit": {"EXIT", "LEAVE", "QUIT", "Q"},
            "help": {"HELP"},
            "back": {"BACK", "RETURN"},
            "root": {"ROOT"}
        }
        self.module_commands = []
        self.command_file_list = command_file_list
        self.load_tree()

        self.stopped = False

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
            prohibited_keywords = set().union(*self.global_commands.values())

            for command in data["commands"]:
                command["target"] = command["target"].upper()
                if command["target"] in prohibited_keywords:
                    exit("Used keyword {} as target. Using keywords is prohibited!".format(command["target"]))
                current_node = self.root_node

                # Per path checking if it has a child
                command["path"] = command["path"].upper()
                for path_piece in command["path"].split(" "):
                    if path_piece in prohibited_keywords:
                        exit("Used keyword {} as target. Using keywords is prohibited!".format(command["target"]))

                    # If the current path info already exists, traverse the tree
                    # Else, add the missing link

                    if path_piece in current_node:
                        current_node = current_node[path_piece]
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

        self.current_node = self.root_node

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
    Starts a new thread asking the user for input and writes this input to the given input_queue
    Optional string for input
    """
    @staticmethod
    def ask_input(input_queue:queue.Queue, string=""):
        i = input(string)
        input_queue.put(i)

    """
    Starts an infinite loop (until exit command is called) which polls for input
    """
    def run_cli(self):
        if not self.input_thread.isAlive() and self.input_queue.empty():
            s = self.make_path_string(self.current_node.get_branch_names()) + " "
            self.input_thread = threading.Thread(target=self.ask_input, args=(self.input_queue, s,))
            self.input_thread.daemon = True
            self.input_thread.start()
        else:
            user_command_list = self.input_queue.get().split(" ")
            for user_word in user_command_list:

                # Step 1: Check for globals
                is_global = False
                for command_type in self.global_commands:
                    if user_word.upper() in self.global_commands[command_type]:
                        is_global = True
                        if command_type == "exit":
                            self.stop()
                        elif command_type == "help":
                            self.print_help(self.current_node)
                        elif command_type == "back":
                            if self.current_node.parent:
                                self.current_node = self.current_node.parent
                        elif command_type == "root":
                            self.current_node = self.root_node

                # Step 2: Check for children
                if not is_global:
                    if user_word.upper() in self.current_node:
                        self.current_node = self.current_node[user_word.upper()]

                    elif len(self.current_node.parameter_list) > 0:
                        print("Command called with {} parameters: {}".format(
                            len(user_command_list[user_command_list.index(user_word):]),
                            "(" + ",".join(user_command_list[user_command_list.index(user_word):]) + ")"
                        ))
                        break

                    else:
                        print("Command {} not found, possible commands: {}".format(user_word, ", ".join(node.name for node in self.current_node.values())))
                        break

    """
    Main loop of the module
    """
    def process(self):
        while self.comm.has_data():
            frame = self.comm.get_data()

        self.run_cli()

    """
    Stops the CLIController
    """
    def stop(self):
        if self.input_thread:
            self.input_thread.join()
        self.comm.stop()
        self.stopped = True