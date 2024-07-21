import socket
import pickle
import threading as thg
import time
from packetstructs import PacketStruct as _ps


class PacketStruct(_ps):
    def __repr__(self):
        return (f"PacketStruct({self.x}, {self.y}, {self.t},"
                f" last_ping: {self.lp}), idle: {self.i}")


def remove_disconnected():
    while True:
        print(f"{player_position}", end="\r")
        for player in player_position.items():
            if time.time() > player[1].lp + 2.5:
                player_position[player[0]].i = True


def run_server():
    print("Running Server")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((SERVER_IP, SERVER_PORT))
        while True:
            data, addr = server_socket.recvfrom(2048)
            data: PacketStruct = pickle.loads(data)
            # print(f"Data Recieved: {data}")

            if data.v == "0.0.1":
                player_position[data.u] = data
                concise_dict = {}
                for p in player_position.items():
                    if not p[1].i:
                        concise_dict[p[0]] = p[1]
                server_socket.sendto(pickle.dumps(concise_dict), addr)
            else:
                server_socket.sendto(b"Wrong Version", addr)


if __name__ == '__main__':
    SERVER_IP = "192.168.1.72"
    SERVER_PORT = 64321
    player_position: dict[str: PacketStruct] = {}

    thg.Thread(target=run_server).start()
    thg.Thread(target=remove_disconnected).start()
