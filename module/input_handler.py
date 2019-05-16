import threading
import queue




class input_handler():
    def __init__(self, cli_controller):
        self.cli_controller = cli_controller
        self.input_queue = queue.Queue()
        self.input_thread = threading.Thread()
    
    def handle_nonglobal_commands(self, user_word, user_command_list):
        """
        Handles all non-global commands. Returns false if failed or if a function has been executed(in this case no other commands can be executed after).
        Returns true if another command can be executed after this one
        """
        if user_word.upper() in self.cli_controller.current_node.keys():
            self.cli_controller.current_node = self.cli_controller.current_node[user_word.upper()]
            return True

        elif len(self.cli_controller.current_node.parameter_list) > 0:
            print("\tCommand called with {} parameters: {}".format(
                len(user_command_list[user_command_list.index(user_word):]),
                "(" + ",".join(user_command_list[user_command_list.index(user_word):]) + ")"
            ))

        elif user_word:
            print("\tCommand {} not found, type \"help\" for possible commands.".format(user_word))
        return False

    
    def handle_new_input(self, input_commands):
        """
        Execute a command depending on text entered
        """
        for user_word in input_commands:
            # Step 1: Check for global commands
            if user_word.upper() in self.cli_controller.global_commands.keys():
                self.cli_controller.global_commands[user_word.upper()]()
                    
            # Step 2: Check for location(in tree structure) specific commands
            else:
                if not self.handle_nonglobal_commands(user_word, input_commands):
                    break

    @staticmethod
    def ask_input(input_queue: queue.Queue, string=""):
        """
        Starts a new thread asking the user for input and writes this input to the given input_queue
        Optional string for input
        """
        i = input(string)
        input_queue.put(i)

    def start_thread(self):
        """
        Starts a new thread to make nonblocking input possible. And get the current location, after restart this is always just root
        """
        s = self.cli_controller.make_path_string(self.cli_controller.current_node.get_branch_names()) + " "
        self.input_thread = threading.Thread(target=self.ask_input, args=(self.input_queue, s))
        self.input_thread.daemon = True
        self.input_thread.start()

    def check_input(self):
        """
        Starts thread asking for input if it is currently not and the input_queue is not filled.
        Otherwise processes items in the input_queue.
        """
        if not self.input_thread.isAlive() and self.input_queue.empty():
            self.start_thread()
        elif not self.input_queue.empty():
            self.handle_new_input(self.input_queue.get().split(" "))