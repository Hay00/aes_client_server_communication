import socket
import os
from dotenv import load_dotenv
from aes import decrypt


def main():
    print(f'[Server] - Started Server, pid: {os.getpid()}')

    # Get secret key to encrypt data
    load_dotenv()
    secret = os.getenv('secret_key').encode('UTF-8')
    length = len(secret)
    if not (length == 16 or length == 24 or length == 32):
        raise ValueError("Secret key must have 16, 24 or 32 length")
    key = bytes(secret)

    # Setup server
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()

    print(f'[Server] - New connection from: {str(address)}')
    while True:
        nonce = conn.recv(16)
        tag = conn.recv(16)
        cipher_text = conn.recv(1024)
        if not cipher_text:
            break  # No data received

        print('\n[Server] - Received data')
        plaintext = decrypt(key, nonce, cipher_text, tag)
        if plaintext:
            print(f'Encrypted: {str(cipher_text.hex())}')
            print(f'Decrypted: {str(plaintext)}')
            conn.send(plaintext.encode())
        else:
            print('Something went wrong, unable to decrypt message')
            conn.send('Error decrypting message'.encode())

    conn.close()


if __name__ == '__main__':
    main()
