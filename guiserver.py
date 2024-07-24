import tkinter as tk
from tkinter import ttk
import threading
import time
import queue
import socket
import pickle
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


# Assuming PacketStruct is defined elsewhere
# from your_module import PacketStruct

SERVER_IP = "192.168.1.72"
SERVER_PORT = 64321


class ThreadedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Threaded Application GUI")
        self.root.geometry("600x400")

        self.player_data = {}
        self.scraper_thread = None
        self.editor_thread = None
        self.stop_event = threading.Event()
        self.update_queue = queue.Queue()

        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the treeview
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, expand=True, fill='both')

        # Create the treeview
        self.tree = ttk.Treeview(tree_frame, columns=('Value', 'Inactive'), show='tree headings')
        self.tree.heading('Value', text='Value')
        self.tree.heading('Inactive', text='Inactive')
        self.tree.pack(side='left', expand=True, fill='both')

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Create buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(btn_frame, text="Start Threads", command=self.start_threads)
        self.start_btn.pack(side='left', padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="Stop Threads", command=self.stop_threads, state='disabled')
        self.stop_btn.pack(side='left', padx=5)

        # Start the update checker
        self.root.after(100, self.check_update_queue)

    def start_threads(self):
        self.stop_event.clear()
        self.scraper_thread = threading.Thread(target=self.scraper_function)
        self.editor_thread = threading.Thread(target=self.editor_function)

        self.scraper_thread.start()
        self.editor_thread.start()

        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')

    def stop_threads(self):
        self.stop_event.set()

        # Wait for threads to finish with a timeout
        timeout = 5  # 5 seconds timeout
        self.scraper_thread.join(timeout)
        self.editor_thread.join(timeout)

        if self.scraper_thread.is_alive() or self.editor_thread.is_alive():
            print("Warning: Some threads didn't stop in time. They will exit on their next iteration.")

        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')

    def scraper_function(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((SERVER_IP, SERVER_PORT))
            server_socket.settimeout(1)  # Set a timeout of 1 second

            while not self.stop_event.is_set():
                try:
                    packet_size, addr = server_socket.recvfrom(64)
                    data, addr = server_socket.recvfrom(int(packet_size.decode()))
                    data = pickle.loads(data)
                    print(f"Data Received: {data}")

                    if data.v != "0.0.2":
                        server_socket.sendto(b"Wrong Version", addr)
                        break

                    self.player_data[data.pi.u] = data.pi
                    concise_dict = {k: v for k, v in self.player_data.items() if not v.i}
                    sending_info = pickle.dumps(ServerPacketStruct(concise_dict, []))

                    server_socket.sendto(f"{len(sending_info)}".encode(), addr)
                    server_socket.sendto(sending_info, addr)

                    self.update_queue.put(self.player_data.copy())

                except socket.timeout:
                    # This allows us to periodically check the stop_event
                    continue
                except Exception as e:
                    print(f"Error in scraper function: {e}")
                    if self.stop_event.is_set():
                        break

    def editor_function(self):
        while not self.stop_event.is_set():
            if self.player_data:
                for player in self.player_data.items():
                    if time.time() > player[1].lp + 2.5:
                        self.player_data[player[0]].i = True
                self.update_queue.put(self.player_data.copy())
            time.sleep(0.01)  # Small delay to prevent excessive CPU usage

    def check_update_queue(self):
        try:
            while True:
                data = self.update_queue.get_nowait()
                self.update_treeview(data)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_update_queue)

    def update_treeview(self, data):
        self.tree.delete(*self.tree.get_children())
        for key, value in data.items():
            # Modify this to display relevant attributes of your PacketStruct
            self.tree.insert('', 'end', text=key, values=(str(value), str(value.i)))


if __name__ == "__main__":
    root = tk.Tk()
    app = ThreadedApp(root)
    root.mainloop()
