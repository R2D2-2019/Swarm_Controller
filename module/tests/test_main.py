import sys

sys.path.append("../../")

import module.frame_functions as frame_functions
import module.command_node as command_node
import module.command_tree_generator as command_tree_generator
from module.cli_controller import CLIController
from module.input_handler import input_handler
import test_frames


# Nodes, Command.send can't be tested yet as there is no mock for Comm yet.
def test_node_init():
    node = command_node.Node("root", node_info="This is a test.")
    assert node.name == "root"
    assert node.node_info == "This is a test."


def test_global_command_execute():
    def func(lst: list) -> int:
        return sum(lst)

    node = command_node.GlobalCommand("TEST", func)

    assert node.func == func
    assert node.execute([10, 12, 20]) == 42


# command_tree_generator, does not yet test command_tree_generator.load_commands
def test_add_frame_commands():
    root_node = command_node.Node("ROOT")
    command_tree_generator.add_frame_commands(root_node, test_frames)

    assert list(root_node.keys()) == ["ROBOT"]
    assert list(root_node["ROBOT"].keys()) == [
        "ACTIVITYLEDSTATE",
        "DISPLAYFILLEDRECTANGLE",
    ]

    for frame in root_node["ROBOT"].values():
        assert frame.node_info

    assert root_node["ROBOT"]["ACTIVITYLEDSTATE"]["state"] is bool

    for param in root_node["ROBOT"]["DISPLAYFILLEDRECTANGLE"].values():
        assert param is int


def test_add_command_from_json():
    command = {
        "name": "test_command",
        "category": "swarm",
        "parameters": ["int x", "int y"],
        "info": "This is a test.",
    }
    root_node = command_node.Node("ROOT")
    command_tree_generator.add_command_from_json(command, root_node, [])

    assert list(root_node.keys()) == ["SWARM"]
    assert list(root_node["SWARM"].keys()) == ["TEST_COMMAND"]

    root_node = command_node.Node("ROOT")
    command_tree_generator.add_command_from_json(
        command, root_node, ["swarm", "test_command"]
    )

    assert list(root_node.keys()) == []


# frame_functions
def test_get_frames_with_description():
    for frame in frame_functions.get_frames_with_description(test_frames):
        assert frame[1].DESCRIPTION

    assert frame_functions.get_frames_with_description(test_frames) == [
        ("FrameActivityLedState", test_frames.FrameActivityLedState),
        ("FrameDisplayFilledRectangle", test_frames.FrameDisplayFilledRectangle),
    ]


# input_handler static methods
def test_print_command_not_found(capsys):
    input_handler._print_command_not_found("test_command")
    assert (
        capsys.readouterr().out
        == "\tCommand 'test_command' not found, type 'help' for possible commands.\n"
    )

def test_check_amount_parameters(capsys):
    lst = ["x", "y"]
    output = input_handler._check_amount_parameters(lst, 2)

    assert output == True

    output = input_handler._check_amount_parameters(lst, 1)

    assert output == False
    assert capsys.readouterr().out == "\tExpected 1 parameters, got 2.\n"

def test_conver_type():
    assert input_handler._convert_type("true", bool) == True
    assert input_handler._convert_type("false", bool) == False
    assert input_handler._convert_type("10", int) == 10
    assert input_handler._convert_type("test", str) == "test"