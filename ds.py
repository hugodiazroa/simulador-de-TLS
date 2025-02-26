import os
import hashlib
import hmac
import binascii
from Crypto.PublicKey import ECC
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Simulated TLS 1.2 Handshake

# Step 1: Client Hello
def client_hello():
    print("=== Client Hello ===")
    client_random = os.urandom(32)
    cipher_suite = "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
    print(f"Client Random: {binascii.hexlify(client_random).decode()}")
    print(f"Cipher Suite: {cipher_suite}")
    return client_random, cipher_suite

# Step 2: Server Hello
def server_hello(client_random):
    print("\n=== Server Hello ===")
    server_random = os.urandom(32)
    session_id = os.urandom(32)
    selected_cipher_suite = "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
    print(f"Server Random: {binascii.hexlify(server_random).decode()}")
    print(f"Session ID: {binascii.hexlify(session_id).decode()}")
    print(f"Selected Cipher Suite: {selected_cipher_suite}")
    return server_random, session_id, selected_cipher_suite

# Step 3: Server Certificate
def server_certificate():
    print("\n=== Server Certificate ===")
    # Simulate a server certificate (in real TLS, this would be an X.509 certificate)
    server_cert = "-----BEGIN SERVER CERTIFICATE-----\n...\n-----END SERVER CERTIFICATE-----"
    print("Server Certificate Sent")
    return server_cert

# Step 4: Server Key Exchange
def server_key_exchange():
    print("\n=== Server Key Exchange ===")
    # Simulate ECDHE parameters
    curve_name = "secp256r1"
    server_private_key = ECC.generate(curve=curve_name)
    server_public_key = server_private_key.public_key()
    print(f"Curve: {curve_name}")
    print(f"Server Public Key: {server_public_key.export_key(format='PEM')}")
    return server_private_key, server_public_key

# Step 5: Server Hello Done
def server_hello_done():
    print("\n=== Server Hello Done ===")
    print("Server has finished its part of the handshake.")

# Step 6: Client Key Exchange
def client_key_exchange(server_public_key):
    print("\n=== Client Key Exchange ===")
    # Simulate client generating its ECDHE key pair
    client_private_key = ECC.generate(curve="secp256r1")
    client_public_key = client_private_key.public_key()
    print(f"Client Public Key: {client_public_key.export_key(format='PEM')}")
    return client_private_key, client_public_key

# Step 7: Key Derivation
def derive_keys(client_random, server_random, client_private_key, server_public_key):
    print("\n=== Key Derivation ===")
    # Simulate shared secret generation (in real TLS, this would use ECDHE)
    shared_secret = os.urandom(32)  # Simulated shared secret
    print(f"Shared Secret: {binascii.hexlify(shared_secret).decode()}")

    # Simulate master secret derivation (in real TLS, this would use a PRF)
    master_secret = hashlib.sha256(client_random + server_random + shared_secret).digest()
    print(f"Master Secret: {binascii.hexlify(master_secret).decode()}")

    # Simulate key derivation (in real TLS, this would use a PRF)
    key_material = hashlib.sha256(master_secret).digest()
    client_write_key = key_material[:16]  # Simulated AES-128 key
    server_write_key = key_material[16:32]  # Simulated AES-128 key
    print(f"Client Write Key: {binascii.hexlify(client_write_key).decode()}")
    print(f"Server Write Key: {binascii.hexlify(server_write_key).decode()}")
    return client_write_key, server_write_key

# Step 8: Change Cipher Spec
def change_cipher_spec():
    print("\n=== Change Cipher Spec ===")
    print("Switching to encrypted communication.")

# Step 9: Finished
def finished(role, key, handshake_messages):
    print(f"\n=== {role} Finished ===")
    # Simulate verification data (in real TLS, this would use HMAC)
    verify_data = hmac.new(key, handshake_messages, hashlib.sha256).digest()
    print(f"Verify Data: {binascii.hexlify(verify_data).decode()}")
    return verify_data

# Step 10: Application Data
def send_application_data(message, key):
    print("\n=== Application Data ===")
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_message = iv + cipher.encrypt(pad(message.encode(), AES.block_size))
    print(f"Encrypted Message: {binascii.hexlify(encrypted_message).decode()}")
    return encrypted_message

def receive_application_data(encrypted_message, key):
    iv = encrypted_message[:16]
    encrypted_message = encrypted_message[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size)
    print(f"Decrypted Message: {decrypted_message.decode()}")

# Main Simulation
def simulate_tls_handshake():
    # Step 1: Client Hello
    client_random, cipher_suite = client_hello()

    # Step 2: Server Hello
    server_random, session_id, selected_cipher_suite = server_hello(client_random)

    # Step 3: Server Certificate
    server_cert = server_certificate()

    # Step 4: Server Key Exchange
    server_private_key, server_public_key = server_key_exchange()

    # Step 5: Server Hello Done
    server_hello_done()

    # Step 6: Client Key Exchange
    client_private_key, client_public_key = client_key_exchange(server_public_key)

    # Step 7: Key Derivation
    client_write_key, server_write_key = derive_keys(client_random, server_random, client_private_key, server_public_key)

    # Step 8: Change Cipher Spec
    change_cipher_spec()

    # Step 9: Client Finished
    handshake_messages = client_random + server_random + client_public_key.export_key(format='DER')
    client_finished = finished("Client", client_write_key, handshake_messages)

    # Step 10: Server Change Cipher Spec
    change_cipher_spec()

    # Step 11: Server Finished
    server_finished = finished("Server", server_write_key, handshake_messages)

    # Step 12: Application Data
    message = "hello"
    encrypted_message = send_application_data(message, client_write_key)

    # Ensure the same key is used for decryption
    print("encrypted_message: ", encrypted_message)
    print("client_write_key: ", client_write_key)
    receive_application_data(encrypted_message, client_write_key)


# Run the simulation
simulate_tls_handshake()