import json
import inspect
import re

import common.frames

from module.command_node import Node, Command
from module.frame_functions import get_frames_with_description

# Regex to detect capital letters (for use in Camelcase to dashed)
CAMEL_REGEX = re.compile("(?!^)([A-Z]+)")


def add_frame_commands(node: Node, mod=common.frames) -> None:
    """
    Adds all commands from the mod file.
    node is the node to which all the commands will be added.
    mod is the module from which to add the frame commands.
    """
    # check if the robot category already exists, otherwise create it
    if not "ROBOT" in node:
        node["ROBOT"] = Node("ROBOT")

    commands = get_frames_with_description(mod)

    # add all commands to root node
    for command in commands:
        # indexes everything of the frame name after 'Frame'
        name = command[0][5:]

        # Converts the camelcase framenames to dashed names (e.g. 'MyCommand' becomes 'my-command')
        name = CAMEL_REGEX.sub(r"-\1", name).upper()

        # get parameters from the frame class
        parameters = inspect.getfullargspec(command[1].set_data).annotations
        description = command[1].DESCRIPTION

        command = Command(name, description)
        command.update(parameters)

        node["ROBOT"][name] = command


def add_command_from_json(
    json_command: dict, node: Node, prohibited_words: list
) -> None:
    """
    add one json command to root node
    """
    name = json_command["name"].upper()
    category = json_command["category"].upper()

    prohibited_words = map(str.upper, prohibited_words)

    if name in prohibited_words:
        print(
            "Used keyword {} as command name. Using keywords is prohibited!".format(
                name
            )
        )
        return

    # Creates the caterogy if it doesn't already exist
    if category not in node:
        node[category] = Node(category)

    # Add the command to the category
    command = Command(name, json_command["info"])
    for parameter in json_command["parameters"]:
        parameter = parameter.split()
        command[parameter[1]] = eval(parameter[0])

    node[category][name] = command


def load_commands(node: Node, prohibited_words: list = None, file: str = None) -> None:
    """
    Loads a single JSON file into the given node
    And loads all the frames from common.frames.py to the command structure
    """
    if file:
        with open(file, "r") as json_file:
            data = json.load(json_file)
        try:
            # Add all commands from previously collected data
            for command in data["commands"]:
                add_command_from_json(command, node, prohibited_words)
        except KeyError as error:
            print("Key {} was not found".format(error))

    # Add all commands from the cpp frames
    add_frame_commands(node)
