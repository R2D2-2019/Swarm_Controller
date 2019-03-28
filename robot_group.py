from robot import robot

class robot_group:
    def __init__(self, tmp_lst_robots):
        print(tmp_lst_robots)
        assert(all([type(a) is robot for a in tmp_lst_robots]))
        self.robot_list = tmp_lst_robots

    def add(self, tmp_robot):
        assert(type(tmp_robot) is robot)
        self.robot_list.append(tmp_robot)
