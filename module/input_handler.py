
from module.command_node import NodeType

class input_handler():
    def __init__(self, cli_controller):
        self.cli_controller = cli_controller

    @staticmethod
    def print_command_not_found(command: str) -> None:
        """
        Prints command not found text with the command parameter.
        """
        print("\tCommand '{}' not found, type 'help' for possible commands.".format(command))

    def handle_help(self, help_parameters):
        try:
            node = self.cli_controller.current_node

            for param in help_parameters:
                node = node[param.upper()]

            self.cli_controller.print_help(node)
        except IndexError:
            self.cli_controller.print_help(self.cli_controller.current_node)
        except KeyError:
            self.print_command_not_found(param)

    def handle_nonglobal_commands(self, user_word, user_command_list) -> bool:
        """
        Handles all non-global commands. Returns false if failed or if a function has been executed(in this case no other commands can be executed after).
        Returns true if another command can be executed after this one
        """

        if user_word.upper() not in self.cli_controller.current_node.keys():
            self.print_command_not_found(user_word)
            return False

        if self.cli_controller.current_node[user_word.upper()].type == NodeType.COMMAND:
            user_params = user_command_list[user_command_list.index(user_word) + 1:]
            command_params = self.cli_controller.current_node[user_word.upper()].parameter_list

            if len(user_params) < len(command_params):
                print("\tToo few commands.")
                return
            elif len(user_params) > len(command_params):
                print("\tToo many commands")
                return

            for i, param in enumerate(command_params):
                try:
                    if command_params[param] is bool:
                        if user_params[i].upper() == "TRUE":
                            user_params[i] = True
                            continue
                        elif user_params[i].upper() == "FALSE":
                            user_params[i] = False
                            continue

                        user_params[i] = bool(int(user_params[i]))
                    elif command_params[param] is int:
                        user_params[i] = int(user_params[i])
                except ValueError:
                    print("\tInvalid type for parameter {} '{}', expected '{}'".format(i, param, command_params[param]))
            return True

        self.cli_controller.current_node = self.cli_controller.current_node[user_word.upper()]
        return False


    def handle_new_input(self, input_commands) -> None:
        """
        Execute a command depending on text entered
        """
        for i, user_word in enumerate(input_commands):
            # Help is a special case, we need to check this first
            if user_word.upper() == "HELP":
                help_parameters = input_commands[i + 1:]
                self.handle_help(help_parameters)
                break

            # Step 2: Check for global commands
            elif user_word.upper() in self.cli_controller.global_commands.keys():
                self.cli_controller.global_commands[user_word.upper()]()

            # Step 3: Check for location(in tree structure) specific commands
            else:
                if self.handle_nonglobal_commands(user_word, input_commands):
                    break



