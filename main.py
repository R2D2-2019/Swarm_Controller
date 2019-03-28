from controller import controller

controller = controller()

while(True):
    command_word = controller.collect_input()

    #Check to see if this is a command callable form anywhere
    controller.process_command_word(command_word)
