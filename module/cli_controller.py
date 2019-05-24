import threading
import queue

import common.frames
from client.comm import BaseComm

from module.command_node import Node
from module.command_tree_generator import load_commands
from module.input_handler import input_handler


class CLIController:
    def __init__(self, comm: BaseComm, command_file_list=None):
        """
        Filenames given have to be JSON files.
        """
        self.comm = comm
        self.input_queue = queue.Queue()
        self.input_thread = threading.Thread()
        self.input_handler = input_handler(self)

        # These function as preserved keywords, do not use these names in commands

        self.global_commands = {
            "EXIT": self.stop,
            "LEAVE": self.stop,
            "QUIT": self.stop,
            "Q": self.stop,
            "HELP": self.print_help,
            "SET": self.set_target,
            "SELECT": self.set_target,
        }

        self.categories = dict()
        self.current_node = self.categories

        self.load_tree(command_file_list)

        # this needs to be requested from swarm, for now this is a mock
        self.possible_targets = {
            "123": self.categories["ROBOT"],
            "321": self.categories["ROBOT"],
        }

        self.stopped = False
        self.target = None

    def load_tree(self, command_file_list) -> None:
        """
        Loads all files into command structure
        """
        for file in command_file_list:
            load_commands(self.categories, self.global_commands, file)

    def set_target(self, params) -> None:
        self.target = (params[0].upper(), self.possible_targets[params[0]])

    # should print info of root node (global commands and categories) and of the currently selected target
    def print_help(self, params: list) -> None:
        """
        Prints the info and any children or parameters of the node.
        """
        print("( HELP )")
        print(
            "\tPossible targets (name: category): {}".format(
                ", ".join(
                    "{}: {}".format(key, value.name)
                    for key, value in self.possible_targets.items()
                )
            )
        )
        print(
            "\tGlobal commands: {}".format(
                ", ".join(command for command in self.global_commands.keys())
            )
        )

        if self.target:
            print(
                "\n\tCurrently selected {}: {}".format(
                    self.target[1].name, self.target[0]
                )
            )
            print(
                "\tTarget specific commands: {}".format(
                    ", ".join(command for command in self.target[1].keys())
                )
            )
        else:
            print("\tNo target selected.")

    @staticmethod
    def ask_input(input_queue: queue.Queue, string="") -> None:
        """
        Starts a new thread asking the user for input and writes this input to the given input_queue
        Optional string for input
        """
        input_queue.put(input(string))

    def start_thread(self) -> None:
        """
        Starts a new thread to make nonblocking input possible. And get the current location, after restart this is always just root
        """
        path_string = "CLI: "
        self.input_thread = threading.Thread(
            target=self.ask_input, args=(self.input_queue, path_string)
        )
        self.input_thread.daemon = True
        self.input_thread.start()

    def check_input(self) -> None:
        """
        Starts thread asking for input if it is currently not and the input_queue is not filled.
        Otherwise processes items in the input_queue.
        """
        if not self.input_thread.isAlive() and self.input_queue.empty():
            self.start_thread()
        elif not self.input_queue.empty():
            self.input_handler.handle_input(self.input_queue.get().split(" "))

    def process(self) -> None:
        """
        Main loop of the module
        """
        while self.comm.has_data():
            frame = self.comm.get_data()

        self.check_input()

    def stop(self, params=None) -> None:
        """
        Stops the CLIController
        """
        if self.input_thread:
            self.input_thread.join()
        self.comm.stop()
        self.stopped = True
