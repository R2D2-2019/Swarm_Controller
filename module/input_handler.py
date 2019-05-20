
from module.command_node import NodeType

class input_handler():
    def __init__(self, cli_controller):
        self.cli_controller = cli_controller

    def handle_nonglobal_commands(self, user_word, user_command_list) -> bool:
        """
        Handles all non-global commands. Returns false if failed or if a function has been executed(in this case no other commands can be executed after).
        Returns true if another command can be executed after this one
        """

        if user_word.upper() not in self.cli_controller.current_node.keys():
            print("\tCommand '{}' not found, type 'help' for possible commands.".format(user_word))
            return False

        if self.cli_controller.current_node[user_word.upper()].type == NodeType.COMMAND:
            if len(self.cli_controller.current_node[user_word.upper()].parameter_list) > 0:
                print("\tCommand called with {} parameters: {}".format(
                    len(user_command_list[user_command_list.index(user_word) + 1:]),
                    "(" + ", ".join(user_command_list[user_command_list.index(user_word) + 1:]) + ")"
                ))
            return True

        self.cli_controller.current_node = self.cli_controller.current_node[user_word.upper()]
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
                if self.handle_nonglobal_commands(user_word, input_commands):
                    break



