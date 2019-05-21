import json
import inspect

import common.frames

from module.command_node import NodeType, Node
from module.frame_functions import get_frames_with_description


def add_command(parent, name, parameters, description) -> None:
    """
    Add one command with all the required information
    """
    target_node = Node(
        name,
        NodeType.COMMAND,
        parameter_list=parameters,
        command_info=description
    )
    target_node.set_parent(parent)
    parent[target_node.name] = target_node

def add_frame_commands(root_node, mod=common.frames) -> None:
    """
    Adds all commands from the mod file
    """
    #check if robot already exists, otherwise create it
    if not 'ROBOT' in root_node:
        root_node["ROBOT"] = Node("ROBOT", NodeType.CATEGORY, root_node)
    current_node = root_node["ROBOT"]

    commands = get_frames_with_description(mod)

    #add all commands to root node
    for command in commands:
        name = command[0][5:]
        parameters = inspect.getfullargspec(command[1].set_data).annotations
        description = command[1].DESCRIPTION
        add_command(current_node, name, parameters, description)


def add_command_from_json(json_command, root_node, prohibited_words) -> None:
    """
    add one json command to root node
    """
    if prohibited_words:
        prohibited_keywords = set().union(prohibited_words)
    json_command["target"] = json_command["target"].upper()
    current_node = root_node

    # Per path checking if it has a child
    json_command["category"] = json_command["category"].upper()
    for path_piece in json_command["category"].split(" "):
        if prohibited_words and path_piece in prohibited_keywords:
            exit("Used keyword {} as target. Using keywords is prohibited!".format(json_command["target"]))

        # If the current path info already exists, traverse the tree
        # Else, add the missing link

        if path_piece in current_node:
            current_node = current_node[path_piece]
        else:
            # Creates the caterogy if it doesn't exist already
            new_node = Node(path_piece, NodeType.CATEGORY, current_node)
            new_node.set_parent(current_node)
            current_node[new_node.name] = new_node
            current_node = new_node

    # After all the missing links in the tree are made, add the command

    add_command(current_node, json_command["target"], json_command["parameters"], json_command["info"])


def load_commands(root_node, prohibited_words=None, file=None) -> None:
    """
    Loads a single JSON file into command structure
    And loads all the frames from common.frames.py to the command structure
    """
    if file:
        with open(file, "r") as json_file:
            data = json.load(json_file)
    try:
        # Add all commands from previously collected data
        for command in data["commands"]:
            add_command_from_json(command, root_node, prohibited_words)
    except KeyError as error:
        print("Key {} was not found".format(error))

    # Add all commands from the cpp frames
    add_frame_commands(root_node)