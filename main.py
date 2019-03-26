from command import command_node

# UTILITY FUNCTION
def list_to_tree(node_names):
    return " \\ ".join(node_names)
#

return_keywords = ["BACK", "RETURN"]
root = command_node("Root")


global_commands = command_node("Global", root)
help_command = command_node("Help", global_commands)
help_command.set_function("This is the help menu")
show_command = command_node("Show", global_commands)
ping_robot = command_node("Ping robot", global_commands)

show_robots = command_node("Robots", show_command)
show_groups = command_node("Groups", show_command)
show_command.add(show_robots)
show_command.add(show_groups)

global_commands.add(show_command)
global_commands.add(ping_robot)

root.add(global_commands)
commands_from_everywhere = {help_command.name : help_command}

current_node = root
while(True):
    command_word = input("{}: ".format(list_to_tree(current_node.get_parents())))
    #Check to see if this is a command callable form anywhere

    if command_word.upper() in commands_from_everywhere:
        last_node = current_node
        current_node = commands_from_everywhere[command_word.upper()]
        if(not current_node.get_child_amount()):
            current_node.do_function()
            current_node = last_node
            if(current_node.get_child_amount()):
                print("Possible keys: ")
                current_node.show_children()


    #return one step in the tree
    elif command_word.upper() in return_keywords:
        if current_node.parent is not None:
            current_node = current_node.parent
    #Check if the command given is in the children of the current node
    elif current_node.has_child(command_word):
        current_node = current_node.get_child(command_word)
    #No children foud print steps to be taken
    else:
        print("==========")
        print("Key not found")
        if(current_node.get_child_amount()):
            print("Possible keys: ")
            current_node.show_children()
        else:
            print("No commands found")
        print("Type return or back to go back one step")
        print("==========")
