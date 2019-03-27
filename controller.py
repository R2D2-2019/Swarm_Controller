from command import command_node
from sys import exit

class controller:
    def __init__(self):
        self.return_keywords = ["BACK", "RETURN"]
        self.exit_keywords = ["EXIT" , "LEAVE", "QUIT"]
        self.root = command_node("Root")

        #TODO - More suitable method of command generation / loading
        # Global commands
        help_command = command_node("Help")
        help_command.set_function("Type {} for traversing the tree upwards.\nType {} for leaving the program".format(self.return_keywords, self.exit_keywords))
        show_command = command_node("Show")
        ping_robot = command_node("Ping robot")


        def show(tmp_target):
            if tmp_target is not None and len(tmp_target) and type(tmp_target) is str:
                if tmp_target.upper() == "ROBOTS":
                    print("There are currently no robots connected. This could be because there is no option to do so.")
                elif tmp_target.upper() == "GROUP":
                    print("Grouping is currently unavailable, please defeat the first gym to access this area.")
        
        show_command.set_function(show)


        # Robot commands
        robot_command = command_node("Robot", self.root)
        connect_command = command_node("Connect", robot_command)
        #TODO - Provide better mockup command
        def connect_to(tmp_addr):
            if tmp_addr is not None and len(tmp_addr):
                if '.' in tmp_addr:
                    print("We connect robot via IP-address: {}".format(tmp_addr))
                else:
                    print("We connect robot via ID: {}".format(tmp_addr))

        connect_command.set_function(connect_to)
        robot_command.add(connect_command)


        self.root.add(robot_command)

        # {name : command}
        self.global_commands = {help_command.name : help_command, show_command.name : show_command, ping_robot.name : ping_robot}
        self.layer = self.root


    #root: show robot 1234
    #root -> show.do_function("robot 1234")
    #show -> robot.do_function("1234")

    # 'function -> exit -> return -> layer -> global' = priority
    def process_command_word(self, tmp_command_word = ""):
        #TODO - better filtering function
        keyword = tmp_command_word.split(' ')[0].upper()
        
        #Step 1: Check if command was exit
        if keyword in self.exit_keywords:
            exit()

        #Step 2: Check if command was return
        elif keyword in self.return_keywords:
            if self.layer.parent is not None:
                self.layer = self.layer.parent
        
        #Step 3: Check if command is in current layer
        elif self.layer.has_child(keyword):
            #print("Deze laag heeft {} als kind".format(tmp_command_word))
            self.layer = self.layer.get_child(keyword)
            self.process_command_word(' '.join(tmp_command_word.split(' ')[1:]))
        
        #Step 4: Check if command is in global
        elif keyword in self.global_commands:
            self.global_commands[keyword].do_function(' '.join(tmp_command_word.split(' ')[1:]))

        #Step 5: Check if this layer has a function to call
        elif callable(self.layer.function):
            self.layer.do_function(tmp_command_word)

            
    def collect_input(self):
        return input("{}: ".format(self.list_to_tree(self.layer.get_parents())))

        

    #TODO - more suitable location for function
    def list_to_tree(self, node_names):
        return " \\ ".join(node_names)