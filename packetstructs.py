class PacketStruct:
    def __init__(self, username: str, x_position: float, y_position: float, view_angle: float):
        self.u = username[:25]
        self.x = x_position
        self.y = y_position
        self.t = view_angle