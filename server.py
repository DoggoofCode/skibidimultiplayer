import socket
import pickle
from packetstructs import PacketStruct as _ps


class PacketStruct(_ps):
    def __repr__(self):
        return f"PacketStruct({self.x}, {self.y}, {self.t})"


def main():
    print("Running Server")
    player_position = {}
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((SERVER_IP, SERVER_PORT))
        while True:
            print(f"{player_position}\r")
            data, addr = server_socket.recvfrom(2048)
            data: PacketStruct = pickle.loads(data)
            # print(f"Data Recieved: {data}")
            player_position[data.u] = data
            server_socket.sendto(pickle.dumps(player_position), addr)


if __name__ == '__main__':
    SERVER_IP = "192.168.1.72"
    SERVER_PORT = 64321
    main()
