import tkinter as tk
from tkinter import scrolledtext
import  random
import time
import gnupg
import hashlib


# Initialize GPG objects
gpgClient = gnupg.GPG()
gpgServer = gnupg.GPG()

input_dataClient = gpgClient.gen_key_input(
    name_email='client@example.com',
    passphrase='client_passphrase'
)
input_dataServer = gpgServer.gen_key_input(
    name_email='server@example.com',
    passphrase='server_passphrase'
)
keyClient = gpgClient.gen_key(input_dataClient)
keyServer = gpgServer.gen_key(input_dataServer)

# Export the public keys
public_keyClient = gpgClient.export_keys(keyClient.fingerprint)
public_keyServer = gpgServer.export_keys(keyServer.fingerprint)
#print("Public Key:\n", public_keyClient)

# Export the private keys
private_keyClient = gpgClient.export_keys(keyClient.fingerprint, True, passphrase='client_passphrase')
private_keyServer = gpgServer.export_keys(keyServer.fingerprint, True, passphrase='server_passphrase')
#print("Private Key:\n", private_key)



class TLSVisualizerApp:
    def __init__(self, rain):
        self.debug = False
        self.log_text = None
        self.reset_button = None
        self.stop_button = None
        self.start_button = None
        self.debug_button = None
        self.root = rain
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

#        self.debug_button = tk.Button(button_frame, text="Toggle debug mode", command=self.debug_toggle, bg="blue", fg="black")
#        self.debug_button.pack(side=tk.LEFT, padx=5)

        # Create a scrolled text widget for the log
        self.log_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=50, bg="black", fg="white")
        self.log_text.pack(padx=10, pady=10)

    def start_1_2(self):
        self.log_text.delete(1.0, tk.END)

        self.log_text.tag_configure("explanation", foreground="white")
        self.log_text.tag_configure("server", foreground="blue")
        self.log_text.tag_configure("client", foreground="red")
        self.log_text.tag_configure("note", foreground="grey")

        self.log_text.insert(tk.END, "Simulation of TLS 1.2\n\n", "explanation")
        self.log_text.insert(tk.END, "Server Parameters\n", "explanation")
        self.log_text.insert(tk.END, "TLS uses a X.509 certificate, but for sake of simplicity we will use PGP\n","note")
        self.log_text.insert(tk.END, "Certificate:\n", "server")
        self.log_text.insert(tk.END, "PGP\n", "server")
        self.log_text.insert(tk.END, "Public Key:\n", "server")
        self.log_text.insert(tk.END, public_keyServer, "server")
        #time.sleep(1)  # Add a one-second delay here
        self.log_text.insert(tk.END, "\nPrivate Key:\n", "server")
        self.log_text.insert(tk.END, private_keyServer, "server")
        #time.sleep(1)  # Add a one-second delay here
        self.log_text.see(tk.END)
        self.log_text.insert(tk.END, "\n\nHandshake\n\n", "explanation")
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
        self.log_text.insert(tk.END, "0x1301\n", "server")

        self.log_text.insert(tk.END, "Extensions:\n", "server")
        self.log_text.insert(tk.END, "extensions = []\n", "server")

        #time.sleep(1)  # Add a one-second delay here

        self.log_text.insert(tk.END, "\n\nServer send certificate chain\n\n", "explanation")
        self.log_text.insert(tk.END, "The server sends a certificate chain to the client")

        self.log_text.insert(tk.END, "\nClient Key Exchange\n\n", "explanation")
        self.log_text.insert(tk.END, "The client sends a pre-master secret to the server, encrypted with the server's public key.\n", "explanation")
        self.log_text.insert(tk.END, "Pre-master secret:\n", "client")

        self.log_text.see(tk.END)








    def start_1_3(self):
        self.log_text.delete(1.0, tk.END)

        self.log_text.tag_configure("explanation", foreground="white")
        self.log_text.tag_configure("server", foreground="blue")
        self.log_text.tag_configure("client", foreground="red")
        self.log_text.tag_configure("note", foreground="grey")

        self.log_text.insert(tk.END, "Simulation of TLS 1.3\n\n", "explanation")
        self.log_text.insert(tk.END, "Server Parameters\n", "explanation")
        self.log_text.insert(tk.END, "TLS uses a X.509 certificate, but for sake of simplicity we will use PGP\n","note")
        self.log_text.insert(tk.END, "Certificate:\n", "server")
        self.log_text.insert(tk.END, "PGP\n", "server")
        self.log_text.insert(tk.END, "Public Key:\n", "server")
        self.log_text.insert(tk.END, public_keyServer, "server")
        self.log_text.insert(tk.END, "\nPrivate Key:\n", "server")
        self.log_text.insert(tk.END, private_keyServer, "server")

        self.log_text.insert(tk.END, "\nHandshake\n\n", "explanation")
        self.log_text.insert(tk.END, "ClientHello\n\n", "explanation")

        self.log_text.insert(tk.END, "The client sends a ClientHello message to the server, containing the following information:\n", "explanation")
        self.log_text.insert(tk.END, "Highest version supported:\n", "client")
        self.log_text.insert(tk.END, "1.3\n", "client")
        prime = 10007
        g = 2
        c = random.getrandbits(10)
        gc = pow(g, c)
        gcmodp= gc % prime
        self.log_text.insert(tk.END, "g^x mod p:\n", "client")
        self.log_text.insert(tk.END, str(gcmodp) + "\n", "client")
        self.log_text.insert(tk.END, "In reality this is a random value, just like the random values sent in TLS 1.2\n", "note")
        self.log_text.insert(tk.END, "For the sake of simplicity, we will use a g^random_value mod p value\n", "note")
        self.log_text.insert(tk.END, "This is a private session key of the client\n", "note")
        self.log_text.insert(tk.END, "This is not sent\n", "note")
        self.log_text.insert(tk.END, "client_session_key = " + str(bin(c)) + "\n", "note")
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
        self.log_text.insert(tk.END, "1.3\n", "server")
        s = random.getrandbits(10)
        gs = pow(g, s)
        gsmodp= gs % prime
        self.log_text.insert(tk.END, "g^s mod p:\n", "server")
        self.log_text.insert(tk.END, str(gsmodp) + "\n", "server")
        self.log_text.insert(tk.END, "not sent: server_session_key = " + str(bin(s)) + "\n", "note")
        self.log_text.insert(tk.END, "Session ID:\n", "server")
        session_id = random.getrandbits(32)
        self.log_text.insert(tk.END, str(bin(session_id)) + "\n", "server")
        self.log_text.insert(tk.END, "Chosen ciphersuite:\n", "server")
        self.log_text.insert(tk.END, "0x1301\n", "server")
        self.log_text.insert(tk.END, "Extensions:\n", "server")
        self.log_text.insert(tk.END, "extensions = []\n", "server")

        self.log_text.insert(tk.END, "\n\nClient sends hash of agreed upon keys\n\n", "explanation")
        self.log_text.insert(tk.END, "With g^s mod p and c, the client can calculate the shared secret\n", "note")
        self.log_text.insert(tk.END, "In order to do this it calculates (g^s mod p)^c mod p\n", "note")
        shared_keyClient = pow(gsmodp, c) % prime
        self.log_text.insert(tk.END, "Shared key (not sent):\n", "note")
        self.log_text.insert(tk.END, str(bin(shared_keyClient)) + "\n", "note")
        self.log_text.insert(tk.END, "The client sends a hash of the shared key to the server\n", "explanation")
        # we will use SHA-256 as the hash function to hash the shared key
        hashClient = hashlib.sha256(str(shared_keyClient).encode()).hexdigest()
        self.log_text.insert(tk.END, "Hash of shared key:\n", "client")
        self.log_text.insert(tk.END, hashClient + "\n", "client")

        self.log_text.insert(tk.END, "\n\n Handshake complete!\n\n", "explanation")

        self.log_text.insert(tk.END, "The handshake is complete, the client and server can now communicate securely\n", "explanation")
        self.log_text.insert(tk.END, "The server should check that its shared key matches the client's shared key\n", "explanation")
        shared_keyServer = pow(gcmodp, s) % prime
        hashServer = hashlib.sha256(str(shared_keyServer).encode()).hexdigest()
        self.log_text.insert(tk.END, "Hash of shared key according to server:\n", "note")
        self.log_text.insert(tk.END, hashServer + "\n", "server")
        self.log_text.insert(tk.END, "Hash of shared key according to client:\n", "note")
        self.log_text.insert(tk.END, hashClient + "\n", "client")







        self.log_text.see(tk.END)

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