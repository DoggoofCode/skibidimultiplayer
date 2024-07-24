class PacketStruct:
    def __init__(self, username: str, x_position: float, y_position: float, view_angle: float, time: int):
        self.u = username[:25]
        self.x = x_position
        self.y = y_position
        self.t = view_angle
        self.lp = time  # last ping
        self.i = False  # idle
        self.v = "0.0.1"  # version


class PlayerStruct:
    def __init__(self,
                 username: str,
                 x: float,
                 y: float,
                 theta: float,
                 attrs: list,
                 time: int):
        self.u = username
        self.x = x
        self.y = y
        self.t = theta
        self.i = False
        self.lp = time
        self.a = {
            "tagged?": attrs[0]
        }


class ClientPacketStruct:
    def __init__(self,
                 player_info: PlayerStruct,
                 action_log: list) -> None:
        self.pi = player_info
        self.log = action_log
        self.v = "0.0.2"


class ServerPacketStruct:
    def __init__(self,
                 players: dict[str:PlayerStruct],
                 environment: list[tuple]):
        self.p = players
        self.env = environment
        self.v = "0.0.2"
