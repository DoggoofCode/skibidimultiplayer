class PacketStruct:
    def __init__(self, username: str, x_position: float, y_position: float, view_angle: float, time: int):
        self.u = username[:25]
        self.x = x_position
        self.y = y_position
        self.t = view_angle
        self.lp = time # last ping
        self.i = False # idle
        self.v = "0.0.1" # version
