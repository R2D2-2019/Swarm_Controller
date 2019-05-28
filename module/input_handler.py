from module.command_node import NodeType
from module.frame_functions import cast_and_send_ui_frame


class input_handler:
    def __init__(self, cli_controller):
        self.cli_controller = cli_controller

    @staticmethod
    def print_command_not_found(command: str) -> None:
        """
        Prints command not found text with the command parameter.
        """
        print("\tCommand '{}' not found, type 'help' for possible commands.".format(command))

    @staticmethod
    def check_amount_parameters(parameters: list, required_amount: int):
        """
        compares the length of the parameters list to the required amount,
        returns true when the length of the parameters is equal to the required amount
        prints to user if not enough or too many parameters
        """
        if len(parameters) < required_amount or len(parameters) > required_amount:
            print("\tExpected {} parameters, got {}.".format(required_amount, len(parameters)))
            return False
        return True

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

    def handle_select(self, select_parameters) -> bool:
        if not self.check_amount_parameters(select_parameters, 1):
            return False
        if not select_parameters[0]:
            print("\tInvalid parameter '{}'".format(select_parameters[0]))
            return False

        self.cli_controller.set_target(select_parameters[0])
        print("\tYou selected {}".format(select_parameters[0]))
        return True

    @staticmethod
    def convert_type(convertable, convert_type):
        if convert_type is bool:
            if convertable.upper() == "TRUE":
                convertable = True
            elif convertable.upper() == "FALSE":
                convertable = False
            else:
                convertable = bool(int(convertable))

        elif convert_type is int:
            convertable = int(convertable)

        return convertable

    def handle_nonglobal_commands(self, user_word, user_command_list) -> bool:
        """
        Handles all non-global commands. Returns false if failed or
        if a function has been executed(in this case no other commands can be executed after).
        Returns true if another command can be executed after this one
        """

        if user_word.upper() not in self.cli_controller.current_node.keys():
            self.print_command_not_found(user_word)
            return False

        if self.cli_controller.current_node[user_word.upper()].type == NodeType.COMMAND:
            if not self.cli_controller.target:
                print("\tNo target selected.")
                return False
            user_params = user_command_list[user_command_list.index(user_word) + 1 :]
            command_params = self.cli_controller.current_node[user_word.upper()].parameter_list

            if not self.check_amount_parameters(user_params, len(command_params)):
                return False

            # Validate if the user parameters are of the correct type.
            # Print invalid type if type is invalid, this code evaluates all parameters.
            correct_params = True
            for i, param in enumerate(command_params):
                try:
                    user_params[i] = self.convert_type(user_params[i], command_params[param])
                except ValueError:
                    print(
                        "\tInvalid type for parameter {} '{}', expected '{}'".format(
                            i, param, command_params[param]
                        )
                    )
                    correct_params = False

            if correct_params:
                print("\tSending command:", user_word, user_params, self.cli_controller.target)
                # below function can currently not be called as there is no string packing support in python bus yet
                # cast_and_send_ui_frame(self.cli_controller.comm, user_word, user_params, self.cli_controller.target)
            return False

        self.cli_controller.current_node = self.cli_controller.current_node[user_word.upper()]
        return True

    def handle_new_input(self, input_commands) -> None:
        """
        Execute a command depending on text entered
        """
        for i, user_word in enumerate(input_commands):
            # Help is a special case, we need to check this first
            if user_word.upper() == "HELP":
                help_parameters = input_commands[i + 1 :]
                self.handle_help(help_parameters)
                break
            # set or select is also a special case
            if user_word.upper() == "SET" or user_word.upper() == "SELECT":
                self.handle_select(input_commands[i + 1 :])
                break

            # Step 3: Check for global commands
            elif user_word.upper() in self.cli_controller.global_commands.keys():
                self.cli_controller.global_commands[user_word.upper()]()

            # Step 4: Check for location(in tree structure) specific commands
            else:
                if not self.handle_nonglobal_commands(user_word, input_commands):
                    break
