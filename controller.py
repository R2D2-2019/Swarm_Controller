from command import command_node
from robot import robot
from robot_group import robot_group
from sys import exit

class controller:
    def __init__(self):
        self.all_robot_list = []
        self.all_group_list = []
        self.return_keywords = ["BACK", "RETURN"]
        self.exit_keywords = ["EXIT" , "LEAVE", "QUIT"]
        self.root = command_node("Root", self)

        #TODO - More suitable method of command generation / loading
        # Global commands
        help_command = command_node("Help", self)
        help_command.set_function("Type {} for traversing the tree upwards.\nType {} for leaving the program".format(self.return_keywords, self.exit_keywords))
        show_command = command_node("Show", self)
        ping_robot = command_node("Ping robot", self)


        def show(self, tmp_target):
            if tmp_target is not None and len(tmp_target) and type(tmp_target) is str:
                if tmp_target.upper() == "ROBOTS":
                    for robot in self.controller.all_robot_list:
                        print("Robot {} is accessible through ip-address {} and at position [{}, {}]".format(robot.id, robot.ip_address, robot.location['x'], robot.location['y']))
                elif tmp_target.upper() == "GROUP":
                    print("Grouping is currently unavailable, please defeat the first gym to access this area.")
        
        show_command.set_function(show)


        # =============== Robot commands ===============
        robot_command = command_node("Robot", self, self.root)



        connect_command = command_node("Connect", self, robot_command)
        #TODO - Connect through Swarm Server
        def connect_to(self, tmp_addr = '0'):
            if tmp_addr is not None and len(tmp_addr):
                if '.' not in tmp_addr:
                    print("First argument is not an IP-address")
                    return
                
                print("We connect robot via IP-address: {}".format(tmp_addr))
                new_connection = robot(0, 0, self.controller.make_new_id(), tmp_addr)
                self.controller.all_robot_list.append(new_connection)
        connect_command.set_function(connect_to)


        move_robot_command = command_node("Move", self, robot_command)
        def move_to(self, command_string):
            args = command_string.split(' ')
            if len(args) < 3:
                print("Not enough parameters to move the robot. Format should be '[robot target] [target x] [target y]")
                return
            robot_target = args[0]
            target_x = args[1]
            target_y = args[2]
            robot = self.controller.get_robot(robot_target)
            if robot is not None:
                robot.move(target_x, target_y)
        move_robot_command.set_function(move_to)


        robot_command.add(move_robot_command)
        robot_command.add(connect_command)
        # ==============================================

        self.root.add(robot_command)

        # {name : command}
        self.global_commands = {help_command.name : help_command, show_command.name : show_command, ping_robot.name : ping_robot}
        self.layer = self.root


    #root: show robot 1234
    #root -> show.do_function("robot 1234")
    #show -> robot.do_function("1234")

    # 'function -> exit -> return -> layer -> global' = priority
    def process_command_word(self, tmp_command_word = ""):
        args = tmp_command_word.split(' ')
        #TODO - better filtering function
        keyword = args[0].upper()
        
        #Step 1: Check if command was exit
        if keyword in self.exit_keywords:
            exit()

        #Step 2: Check if command was return
        elif keyword in self.return_keywords:
            if self.layer.parent is not None:
                self.layer = self.layer.parent
        
        #Step 3: Check if command is in current layer
        elif self.layer.has_child(keyword):
            self.layer = self.layer.get_child(keyword)
            self.process_command_word(' '.join(args[1:]))
        
        #Step 4: Check if command is in global
        elif keyword in self.global_commands:
            self.global_commands[keyword].do_function(' '.join(args[1:]))

        #Step 5: Check if this layer has a function to call
        elif callable(self.layer.function):
            self.layer.do_function(tmp_command_word)

            
    def collect_input(self):
        return input("{}: ".format(self.list_to_tree(self.layer.get_parents())))

    #gets the max id of all the robots, and returns that value + 1 as the new highest id
    #If no robots are currently connected, first id starts at 1
    def make_new_id(self):
        if(len(self.all_robot_list) > 0):
            return max([a.id for a in self.all_robot_list]) + 1
        else:
            return 1

    def get_robot(self, robot_target):
        for robot in self.all_robot_list:
            if '.' in robot_target:
                if robot.ip_address == robot_target:
                    return robot
            else:
                try:
                    if int(robot.id) == int(robot_target):
                        return robot
                except ValueError:
                    print("Invallid argument {} is not convertible to int".format(robot_target))
        print("No robot found for target {}".format(robot_target))
            
    #TODO - more suitable location for function
    def list_to_tree(self, node_names):
        return " \\ ".join(node_names)