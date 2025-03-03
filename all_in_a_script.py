import tkinter as tk
from datetime import datetime, timedelta
from tkinter import scrolledtext
import  random
import time
from cryptography import x509


class TLSVisualizerApp:
    def __init__(self, raiz):
        self.debug = False
        self.log_text = None
        self.reset_button = None
        self.stop_button = None
        self.start_button = None
        self.debug_button = None
        self.root = raiz
        self.root.title("TLS Visualizer")
        self.root.geometry("800x600")  # Set the initial size of the window
        self.root.configure(bg="black")  # Set the background color to black
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the buttons
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        # Add buttons
        self.start_button = tk.Button(button_frame, text="Simulate TLS 1.2", command=self.start_1_2, bg="green", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(button_frame, text="Simulate TLS 1.3", command=self.start_1_3, bg="red", fg="white")
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_simulation, bg="yellow", fg="black")
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.debug_button = tk.Button(button_frame, text="Toggle debug mode", command=self.debug_toggle, bg="blue", fg="black")
        self.debug_button.pack(side=tk.LEFT, padx=5)

        # Create a scrolled text widget for the log
        self.log_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=50, bg="black", fg="white")
        self.log_text.pack(padx=10, pady=10)

    def start_1_2(self):
        self.log_text.tag_configure("explanation", foreground="white")
        self.log_text.tag_configure("server", foreground="blue")
        self.log_text.tag_configure("client", foreground="red")

        self.log_text.insert(tk.END, "Simulation of TLS 1.2\n\n", "explanation")
        self.log_text.insert(tk.END, "Server Parameters\n", "explanation")


        self.log_text.insert(tk.END, "Certificate:\n", "server")

        self.log_text.insert(tk.END, "Public Key:\n", "server")

        self.log_text.insert(tk.END, "Private Key:\n", "server")

        self.log_text.insert(tk.END, "\nHandshake\n\n", "explanation")
        self.log_text.insert(tk.END, "ClientHello\n\n", "explanation")

        self.log_text.insert(tk.END, "The client sends a ClientHello message to the server, containing the following information:\n", "explanation")
        self.log_text.insert(tk.END, "Highest version supported:\n", "client")
        self.log_text.insert(tk.END, "1.3\n", "client")
        self.log_text.insert(tk.END, "Random number with timestamp:\n", "client")
        # we have to generate a 256-bit random number, then replace the first 16 bits with the current timestamp
        client_random_1_2 = random.getrandbits(256)
        if self.debug: self.log_text.insert(tk.END, str(bin(client_random_1_2)) + "\n", "client")
        if self.debug: self.log_text.insert(tk.END, str(client_random_1_2) + "\n", "client")
        client_random_1_2_to_replace = client_random_1_2 % 2**16
        client_random_1_2 = client_random_1_2 - client_random_1_2_to_replace
        if self.debug: self.log_text.insert(tk.END, str(bin(client_random_1_2)) + "\n", "client")
        # we get 16 bits from the current timestamp, in milliseconds
        timestamp = int(time.time() * 1000) % 2**16
        if self.debug: self.log_text.insert(tk.END, str(bin(timestamp)) + "\n", "client")
        client_random_1_2 = client_random_1_2 + timestamp
        if self.debug: self.log_text.insert(tk.END, str(bin(client_random_1_2)) + "\n", "client")
        if self.debug: self.log_text.insert(tk.END, str(client_random_1_2) + "\n", "client")
        self.log_text.insert(tk.END, str(bin(client_random_1_2)) + "\n", "client")
        # the client sends the a session ID, which is empty in this case, and is formatted as a 32-bit number
        session_id = 0
        self.log_text.insert(tk.END, "Session ID:\n", "client")
        self.log_text.insert(tk.END, str(bin(session_id)) + "\n", "client")
        # the client sends a list of supported ciphersuites
        self.log_text.insert(tk.END, "Supported ciphersuites:\n", "client")
        self.log_text.insert(tk.END, "ciphersuites = [0x1301, 0x1302, 0x1303, 0x1304]\n", "client")
        # the client sends a list of extension, we will not include them in this simulation
        self.log_text.insert(tk.END, "Extensions:\n", "client")
        self.log_text.insert(tk.END, "extensions = []\n", "client")

        self.log_text.insert(tk.END, "\nServerHello\n\n", "explanation")

        self.log_text.insert(tk.END, "The server sends a ServerHello message to the client, containing the following information:\n", "explanation")
        self.log_text.insert(tk.END, "Highest version supported:\n", "server")
        self.log_text.insert(tk.END, "1.2\n", "server")

        self.log_text.insert(tk.END, "Random number with timestamp:\n", "server")
        server_random_1_2 = random.getrandbits(256)
        if self.debug: self.log_text.insert(tk.END, str(bin(server_random_1_2)) + "\n", "server")
        if self.debug: self.log_text.insert(tk.END, str(server_random_1_2) + "\n", "server")
        server_random_1_2_to_replace = server_random_1_2 % 2**16
        server_random_1_2 = server_random_1_2 - server_random_1_2_to_replace
        if self.debug: self.log_text.insert(tk.END, str(bin(server_random_1_2)) + "\n", "server")
        # we get 16 bits from the current timestamp, in milliseconds
        timestamp = int(time.time() * 1000) % 2**16
        if self.debug: self.log_text.insert(tk.END, str(bin(timestamp)) + "\n", "server")
        server_random_1_2 = server_random_1_2 + timestamp
        if self.debug: self.log_text.insert(tk.END, str(bin(server_random_1_2)) + "\n", "server")
        if self.debug: self.log_text.insert(tk.END, str(server_random_1_2) + "\n", "server")
        self.log_text.insert(tk.END, str(bin(server_random_1_2)) + "\n", "server")

        self.log_text.insert(tk.END, "Session ID:\n", "server")
        session_id = random.getrandbits(32)
        self.log_text.insert(tk.END, str(bin(session_id)) + "\n", "server")

        self.log_text.insert(tk.END, "Chosen ciphersuite:\n", "server")
        self.log_text.insert(tk.END, "0x1303\n", "server")

        self.log_text.insert(tk.END, "Extensions:\n", "server")
        self.log_text.insert(tk.END, "extensions = []\n", "server")

        time.sleep(1)  # Add a one-second delay here

        self.log_text.insert(tk.END, "\n\nServer send certificate chain\n\n", "explanation")
        self.log_text.insert(tk.END, "The server sends a certificate chain to the client")

        self.log_text.insert(tk.END, "\nClient Key Exchange\n\n", "explanation")
        self.log_text.insert(tk.END, "The client sends a pre-master secret to the server, encrypted with the server's public key.\n", "explanation")
        self.log_text.insert(tk.END, "Pre-master secret:\n", "client")

        self.log_text.see(tk.END)








    def start_1_3(self):
        self.log_text.insert(tk.END, "Simulation of TLS 1.3.\n\n")

    def debug_toggle(self):
        self.debug = not self.debug
        if self.debug:
            self.log_text.insert(tk.END, "Debug mode enabled.\n")
        else:
            self.log_text.insert(tk.END, "Debug mode disabled.\n")

    def reset_simulation(self):
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "Simulation reset.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = TLSVisualizerApp(root)
    root.mainloop()