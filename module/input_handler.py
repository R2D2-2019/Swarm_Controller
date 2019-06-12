from module.command_node import Node, Command


class input_handler:
    """
    Handles input of the given cli_controller.
    """

    def __init__(self, cli_controller):
        """
        cli_controller must be the parent controller and functions will be called on it.

        @param cli_controller
        """
        self.cli_controller = cli_controller

    @staticmethod
    def _print_command_not_found(command: str) -> None:
        """
        Prints command not found text with the command parameter.

        @param str
        """
        print(
            "\tCommand '{}' not found, type 'help' for possible commands.".format(
                command
            )
        )

    @staticmethod
    def _check_amount_parameters(parameters: list, required_amount: int) -> bool:
        """
        compares the length of the parameters list to the required amount.

        returns true when the length of the parameters is equal to the required amount, else false

        @param list
        @param int
        """
        if len(parameters) < required_amount or len(parameters) > required_amount:
            return False
        return True

    @staticmethod
    def _print_expected_parameters(expected: int, got: int) -> None:
        """
        prints the string "Expected {} parameters, got {}." where expected and got are filled in to the {}

        @param int
        @param int
        """
        print("\tExpected {} parameters, got {}.".format(expected, got))

    @staticmethod
    def _convert_type(convertable: str, convert_type: type):
        """
        Converts the convertable into the convert_type,
        when the convert_type is a bool the function will also evaluate "TRUE" and "FALSE".
        returns the type of convert_type

        @param str
        @param type
        """
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

    def handle_select(self, select_parameters: list) -> None:
        """
        Handles the select command,
        which allows the user to set the target from the list of possible targets.
        Seting a target allows the user to execute commands on that target.

        select_parameters is a list containing strings of parameters

        @param list
        """
        if not self._check_amount_parameters(select_parameters, 1):
            self._print_expected_parameters(1, len(select_parameters))
            return
        if not select_parameters[0] in self.cli_controller.possible_targets:
            print("\tInvalid target '{}'".format(select_parameters[0]))
            return

        self.cli_controller.set_target(select_parameters[0])
        print("\tYou selected {}".format(select_parameters[0]))

    def handle_help(self, params: list) -> None:
        """
        Prints general information and information about the target,
        or information about a command if given as a parameter

        params is a list containing strings of parameters

        @param list
        """
        # If a parameter is given this prints the information of that parameter
        if params:
            if not self._check_amount_parameters(params, 1):
                self._print_expected_parameters(1, len(params))
                return

            param = params[0].upper()
            if param in self.cli_controller.global_commands:
                print("( {} )".format(param))
                print("\t" + self.cli_controller.global_commands[param].node_info)
            elif self.cli_controller.target:
                try:
                    node = self.cli_controller.target[1][param]

                    print("( {} )".format(node.name))
                    print("\t" + node.node_info)
                    print(
                        "\n\tParameters (name: type): {}".format(
                            ", ".join(
                                "{}: {}".format(key, value)
                                for key, value in node.items()
                            )
                        )
                    )
                except KeyError:
                    self._print_command_not_found(param)
            else:
                self._print_command_not_found(param)
            return

        # If no parameter is given it prints general information and the selected target's information
        print("( HELP )")
        print(
            "\tPossible targets (category: name): {}".format(
                ", ".join(
                    "{}: {}".format(value.name.lower(), key.lower())
                    for key, value in self.cli_controller.possible_targets.items()
                )
            )
        )
        print(
            "\tGlobal commands: {}".format(
                ", ".join(map(str.lower, self.cli_controller.global_commands.keys()))
            )
        )

        if self.cli_controller.target:
            print(
                "\n\tCurrently selected {}: {}".format(
                    self.cli_controller.target[1].name.lower(),
                    self.cli_controller.target[0].lower(),
                )
            )
            print(
                "\tTarget specific commands: {}".format(
                    ", ".join(map(str.lower, self.cli_controller.target[1].keys()))
                )
            )
        else:
            print("\n\tNo target selected.")

    def _handle_category_command(self, command: str, params: list) -> None:
        """
        Handles all non-global commands. Returns false if failed or
        if a function has been executed(in this case no other commands can be executed after).
        Returns true if another command can be executed after this one

        command is the command to be executed
        params is a list containing strings of parameters
        
        @param str
        @param list
        """
        category = self.cli_controller.target[1]

        if command not in category:
            self._print_command_not_found(command)
            return

        required_params = category[command]

        if not self._check_amount_parameters(params, len(required_params)):
            self._print_expected_parameters(len(required_params), len(params))
            return

        # Validate if the user paramters are of the correct type.
        # Print invalid type if type is invalid, this code evaluates all parameters.
        correct_params = True
        for i, param in enumerate(required_params):
            try:
                params[i] = self._convert_type(params[i], required_params[param])
            except ValueError:
                print(
                    "\tInvalid type for parameter {} '{}', expected '{}'".format(
                        i, param, required_params[param]
                    )
                )
                correct_params = False

        if not correct_params:
            return

        print(
            "\tSending command:",
            command.lower(),
            params,
            " to: ",
            self.cli_controller.target[0].lower(),
        )
        # cant be executed yet as python bus string frames are not working like intended yet
        # category[command].send(
        #    self.cli_controller.comm, params, self.cli_controller.target[0]
        # )

    def _handle_command(self, command: str, params: list):
        """
        Handles a command. It tries to locate the command and then call it using the given params.

        command is the command to be handled
        params is a list containing strings of parameters

        @param str
        @param list
        """
        if command in self.cli_controller.global_commands:
            self.cli_controller.global_commands[command].execute(params)
        elif self.cli_controller.target:
            self._handle_category_command(command, params)
        else:
            self._print_command_not_found(command)
            print(
                """\tMaybe the command you were trying to execute is a target specific command,
\tuse 'select' to select a target."""
            )

    def handle_input(self, input_words: list) -> None:
        """
        Execute a command depending on text entered

        input_words is a list containing a string of user input

        @param list
        """
        command = []
        while input_words:
            word = input_words.pop(0).strip()

            if word == "&&":
                self._handle_command(command[0].upper(), command[1:])
                command = []
                continue

            if word != "":
                command.append(word)

            if input_words == []:
                self._handle_command(command[0].upper(), command[1:])
