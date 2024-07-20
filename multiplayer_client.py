import socket, pygame, pickle, sys
from packetstructs import PacketStruct as _ps


class PacketStruct(_ps):
    def __repr__(self):
        return f"PacketStruct({self.x}, {self.y}, {self.t})"


SERVER_IP = "192.168.1.72"
SERVER_PORT = 64321

username = input("Username?: ")


def main():
    def get_player_data(player_data) -> dict[str, PacketStruct]:
        print(f"Sending: {len(pickle.dumps(PacketStruct(username, x, y, 0)))}, TO; {(SERVER_IP, SERVER_PORT)}")
        client_socket.sendto(pickle.dumps(PacketStruct(username, x, y, 0)), (SERVER_IP, SERVER_PORT))

        print("Waiting for data")
        data, _ = client_socket.recvfrom(2048)

        return pickle.loads(data)

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

        p_data = get_player_data(PacketStruct(username, x, y, 0))

        # Fill the background with white
        window.fill(white)

        # Draw you
        pygame.draw.circle(window, black, (x, y), 20)

        for player in p_data.items():
            if player[0] != username:
                pygame.draw.circle(window, red, (player[1].x, player[1].y), 20)

        pygame.display.flip()
        clock.tick(tps)

    client_socket.close()


if __name__ == '__main__':
    main()
