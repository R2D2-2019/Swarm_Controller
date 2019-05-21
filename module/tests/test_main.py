import sys
sys.path.append("../../")

import module.frame_functions as frame_functions
import module.command_node as command_node
import module.command_tree_generator as command_tree_generator
from module.input_handler import input_handler
import test_frames


# Node
def test_node_init():
    parent = command_node.Node("parent")
    node = command_node.Node(
        "root",
        node_type=command_node.NodeType.ROOT,
        parent=parent,
        parameter_list=["x", "y"],
        command_info="This is a test."
    )
    assert node.name == "ROOT"
    assert node.type == command_node.NodeType.ROOT
    assert node.parent == parent
    assert node.parameter_list == ["x", "y"]
    assert node.command_info == "This is a test."

    first_node = command_node.Node("root")
    second_node = command_node.Node("root")
    first_node.parameter_list.append("x")

    assert second_node.parameter_list == []


def test_node_get_branch_names():
    root_node = command_node.Node("ROOT")
    first_root_child = command_node.Node("FIRST_ROOT_CHILD", parent=root_node)
    second_root_child = command_node.Node("SECOND_ROOT_CHILD", parent=root_node)
    child_of_first_root_child = command_node.Node(
        "CHILD_OF_FIRST_ROOT_CHILD",
        parent=first_root_child
    )

    assert root_node.get_branch_names() == ["ROOT"]
    assert second_root_child.get_branch_names() == [
        "ROOT",
        "SECOND_ROOT_CHILD"
    ]
    assert child_of_first_root_child.get_branch_names() == [
        "ROOT", "FIRST_ROOT_CHILD", "CHILD_OF_FIRST_ROOT_CHILD"
    ]


def test_node_set_parent():
    root_node = command_node.Node("ROOT")
    new_root_node = command_node.Node("NEW_ROOT")
    child_node = command_node.Node("CHILD", parent=root_node)
    child_node.set_parent(new_root_node)

    assert child_node.parent == new_root_node

# command_tree_generator, does not yet test command_tree_generator.load_commands
def test_add_command():
    root_node = command_node.Node("ROOT")
    command_tree_generator.add_command(
        root_node,
        "CHILD",
        ["x", "y"],
        "This is a test."
    )
    test_node = command_node.Node(
        "CHILD",
        node_type=command_node.NodeType.COMMAND,
        parent=root_node,
        parameter_list=["x", "y"],
        command_info="This is a test."
    )

    assert root_node["CHILD"] == test_node
    assert root_node["CHILD"].parent == root_node


def test_add_frame_commands():
    root_node = command_node.Node("ROOT")
    command_tree_generator.add_frame_commands(root_node, test_frames)

    assert list(root_node.keys()) == ["ROBOT"]
    assert list(root_node["ROBOT"].keys()) == [
        "ACTIVITYLEDSTATE",
        "DISPLAYFILLEDRECTANGLE"
    ]

    for frame in root_node["ROBOT"].values():
        assert frame.command_info

    assert root_node["ROBOT"]["ACTIVITYLEDSTATE"].parameter_list["state"] is bool

    for param in root_node["ROBOT"]["DISPLAYFILLEDRECTANGLE"].parameter_list.values():
        assert param is int


def test_add_command_from_json():
    command = {
        "target": "test_command",
        "category": "swarm",
        "parameters": ["x", "y"],
        "info": "This is a test."
    }
    root_node = command_node.Node("ROOT")
    command_tree_generator.add_command_from_json(command, root_node, [])

    assert list(root_node.keys()) == ["SWARM"]
    assert list(root_node["SWARM"].keys()) == ["TEST_COMMAND"]

    root_node = command_node.Node("ROOT")
    command_tree_generator.add_command_from_json(
        command,
        root_node,
        ["swarm", "test_command"]
    )

    assert list(root_node.keys()) == []

# frame_functions, test for cast_and_send_ui_frame can't be implemented yet
# as there is no mock Comm yet.
def test_get_frames_with_description():
    for frame in frame_functions.get_frames_with_description(test_frames):
        assert frame[1].DESCRIPTION

    assert frame_functions.get_frames_with_description(test_frames) == [
        ("FrameActivityLedState", test_frames.FrameActivityLedState),
        ("FrameDisplayFilledRectangle", test_frames.FrameDisplayFilledRectangle)
    ]

# input_handler
def test_print_command_not_found(capsys):
    input_handler.print_command_not_found("test_command")
    assert capsys.readouterr().out == \
    "\tCommand 'test_command' not found, type 'help' for possible commands.\n"