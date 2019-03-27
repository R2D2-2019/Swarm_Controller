from controller import controller

# UTILITY FUNCTION
#
'''
return_keywords = ["BACK", "RETURN"]
root = command_node("Root")



help_command = command_node("Help")
help_command.set_function("This is the help menu")
show_command = command_node("Show")
ping_robot = command_node("Ping robot")

show_robots = command_node("Robots", show_command)
show_groups = command_node("Groups", show_command)
show_command.add(show_robots)
show_command.add(show_groups)

global_commands.add(show_command)
global_commands.add(ping_robot)

root.add(global_commands)
commands_from_everywhere = {help_command.name : help_command, }

current_node = root
'''

controller = controller()

while(True):
    command_word = controller.collect_input()
    #Check to see if this is a command callable form anywhere
    controller.process_command_word(command_word)
    '''
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
    '''