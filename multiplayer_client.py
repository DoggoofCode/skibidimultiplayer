import socket, pygame, pickle, sys, time
from packetstructs import (
    PacketStruct as _ps,
    ClientPacketStruct as _cps,
    ServerPacketStruct as _sps,
    PlayerStruct as _pls,
)


class PacketStruct(_ps):
    def __repr__(self):
        return (f"PacketStruct({self.x}, {self.y}, {self.t},"
                f" last_ping: {self.lp}), idle: {self.i}")


class ClientPacketStruct(_cps):
    def __repr__(self):
        return (f"ClientPacketStruct(Player Info: {self.pi},"
                f" Action Log: {self.log})")


class ServerPacketStruct(_sps):
    def __repr__(self):
        return (f"ClientPacketStruct(Players: {self.p},"
                f" Environment: {self.env})")


class PlayerStruct(_pls):
    def __repr__(self):
        return (f"PlayerData(x:{self.x}, y:{self.y},"
                f" theta:{self.t}, attrs: {self.a})")


SERVER_IP = "192.168.1.72"
SERVER_PORT = 64321

username = input("Username?: ")


def main():
    def get_player_data() -> dict[str, PlayerStruct]:
        # pkt = PacketStruct(username, x, y, 0, int(time.time()))
        ply_inf = PlayerStruct(username, x, y, 0, [False], int(time.time()))
        pkt = ClientPacketStruct(ply_inf, [])

        enc_pkt = pickle.dumps(pkt)

        print(f"Sending: {len(enc_pkt)}, TO: {(SERVER_IP, SERVER_PORT)}")
        client_socket.sendto(f"{len(enc_pkt)}".encode(), (SERVER_IP, SERVER_PORT))
        client_socket.sendto(enc_pkt, (SERVER_IP, SERVER_PORT))

        print("Waiting for data")
        buff_size, _ = client_socket.recvfrom(64)
        data, _ = client_socket.recvfrom(int(buff_size.decode()))
        print(ud := pickle.loads(data))

        return ud.p

    pygame.init()

    # Set up the display
    width, height = 800, 600
    window = pygame.display.set_mode((width, height))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clock = pygame.time.Clock()
    tps = 60
    pygame.display.set_caption('multiplayer game demo')

    # Define colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    x, y = 0, 0
    tagged = False
    # Main loop
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= 4
        if keys[pygame.K_RIGHT]:
            x += 4
        if keys[pygame.K_UP]:
            y -= 4
        if keys[pygame.K_DOWN]:
            y += 4

        print(x, y)

        p_data = get_player_data()

        # Fill the background with white
        window.fill(white)

        # Draw you
        pygame.draw.circle(window,
                           black if not tagged else red,
                           (x, y), 20)

        for player in p_data.items():
            if player[0] != username and not player[1].i:
                pygame.draw.circle(window,
                                   red if player[1].a["tagged?"] else blue,
                                   (player[1].x, player[1].y),
                                   20)

        pygame.display.flip()
        clock.tick(tps)

    client_socket.close()


if __name__ == '__main__':
    main()
