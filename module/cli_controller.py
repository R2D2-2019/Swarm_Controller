import common.frames
from client.comm import BaseComm

from module.command_node import CommandNode
from module.command_tree_generator import load_commands
from module.input_handler import input_handler


class CLIController:

    def __init__(self, comm: BaseComm, command_file_list=None):
        """
        Filenames given have to be JSON files.
        """
        self.comm = comm
        self.root_node = CommandNode("ROOT")

        # These function as preserved keywords, do not use these names in commands

        self.global_commands = {
            "EXIT":     self.stop,
            "LEAVE":    self.stop,
            "QUIT":     self.stop,
            "Q":        self.stop,
            "HELP":     self.print_help,
            "BACK":     self.go_back_in_tree,
            "RETURN":   self.go_back_in_tree,
            "ROOT":     self.go_to_root
        }
        self.command_file_list = command_file_list
        self.load_tree()
        self.current_node = self.root_node

        self.input_handler = input_handler(self)

        self.stopped = False


    def load_tree(self):
        """
        Loads all files into command structure
        """
        for file in self.command_file_list:
            load_commands(self.root_node, self.global_commands, file)

    @staticmethod
    def make_path_string(path_list):
        """
        Joins given list and appends a ':'
        Expects a list
        """
        return ' / '.join(path_list) + ":"

    def print_help(self):
        node = self.current_node
        """
        Prints the info and any children or parameters of the node.
        """
        print(node.name + ":")
        print("\tInfo: " + node.command_info)
        if node.parameter_list:
            print("\tParameters: (" + (", ".join(node.parameter_list)) + ")")
        elif len(node) > 0:
            print("\tPossible commands: {}".format(", ".join(node[n].name.lower() for n in node.keys())))
        else:
            print("\tThis function requires no parameters and has no children")

    def go_back_in_tree(self):
        """
        Go back one node in the tree structure. You cant go back when in root
        """
        if self.current_node.parent:
            self.current_node = self.current_node.parent


    def go_to_root(self):
        """
        Go to root in tree structure
        """
        self.current_node = self.root_node
                
    def process(self):
        """
        Main loop of the module
        """
        while self.comm.has_data():
            frame = self.comm.get_data()

        self.input_handler.check_input()

    def stop(self):
        """
        Stops the CLIController
        """
        if self.input_handler.input_thread:
            self.input_handler.input_thread.join()
        self.comm.stop()
        self.stopped = True
