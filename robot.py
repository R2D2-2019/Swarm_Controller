class robot:
    def __init__(self, tmp_x = 0, tmp_y = 0, tmp_id = 0, tmp_ip_address = '0.0.0.0'):
        self.location = {"x": tmp_x, "y": tmp_y }
        self.id = tmp_id
        self.ip_address = tmp_ip_address

    def move(self, new_x, new_y):
        print("New location [{}, {}]".format(new_x, new_y))
        self.location['x'] = new_x
        self.location['y'] = new_y