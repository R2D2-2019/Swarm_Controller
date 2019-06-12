import threading
import queue

import common.frames
from client.comm import BaseComm

from module.command_node import GlobalCommand
from module.command_tree_generator import load_commands
from module.input_handler import input_handler


class CLIController:
    def __init__(self, comm: BaseComm, command_file_list: list):
        """
        comm must be a BaseComm from the client.comm module (python-bus)

        command_file_list must be a path to a JSON formatted file like such:

        {
            "commands": [
                {
                "name": "command_name",
                "category": "command_category",
                "parameters": [
                    "type parameter_name",
                    "type parameter_name"
                ],
                "info": "Explanation of the command, and how to use it."
                },

                {
                    # next command formatted like the previous
                }
            ]
        }

        @param BaseComm
        @param list
        """

        self.comm = comm
        self.input_queue = queue.Queue()
        self.input_thread = threading.Thread()
        self.input_handler = input_handler(self)

        # These function as preserved keywords, do not use these names in commands
        stop = GlobalCommand("EXIT", self.stop, node_info="Exits the CLI interface.")
        self.global_commands = {
            "EXIT": stop,
            "QUIT": stop,
            "HELP": GlobalCommand(
                "HELP",
                self.input_handler.handle_help,
                node_info="Prints general help or help of given parameter.",
            ),
            "SELECT": GlobalCommand(
                "SELECT",
                self.input_handler.handle_select,
                node_info="Select a target on which to execute commands.",
            ),
        }

        self.categories = dict()

        self.load_tree(command_file_list)

        # this needs to be requested from swarm, for now this is a mock
        self.possible_targets = {
            "rob-with-arm": self.categories["ROBOT"],
            "rob-with-alarm": self.categories["ROBOT"],
            "team-alpha": self.categories["SWARM"],
            "team-beta": self.categories["SWARM"],
        }

        self.stopped = False
        self.target = None

    def load_tree(self, command_file_list: list) -> None:
        """
        Loads all files into command structure

        @param list
        """
        for file in command_file_list:
            load_commands(self.categories, self.global_commands, file)

    def set_target(self, target: str) -> None:
        """
        sets the target

        @param str
        """
        self.target = (target.upper(), self.possible_targets[target])

    @staticmethod
    def ask_input(input_queue: queue.Queue, string: str = "") -> None:
        """
        Starts a new thread asking the user for input and writes this input to the given input_queue
        Optional string for input

        @param Queue
        @param str
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

    def stop(self, params: list = None) -> None:
        """
        Stops the CLIController
        params is a required parameters because stop is a global command, 
        params is not used in this function

        @param list
        """
        if self.input_thread:
            self.input_thread.join()
        self.comm.stop()
        self.stopped = True
