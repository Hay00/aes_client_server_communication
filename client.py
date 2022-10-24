import socket
import os
from dotenv import load_dotenv
from aes import encrypt


def main():
    print(f'[Client] - Started Client, pid: {os.getpid()}')

    # Get secret key to encrypt data
    load_dotenv()
    secret = os.getenv('secret_key').encode('UTF-8')
    length = len(secret)
    if not (length == 16 or length == 24 or length == 32):
        raise ValueError("Secret key must have 16, 24 or 32 length")
    key = bytes(secret)

    # Stablish connection with server
    host = socket.gethostname()
    port = 5000
    client_socket = socket.socket()
    client_socket.connect((host, port))

    print(f'[Client] - Client ')
    for _ in range(5):
        # Get input and encrypt it
        input_text = input('\n[Client] - Enter a message: ')
        nonce, cipher_text, tag = encrypt(key,  input_text)
        print(f'[Client] - Encrypted message: {cipher_text.hex()}')

        # Send nonce, tag and ciphered text
        client_socket.send(nonce)
        client_socket.send(tag)
        client_socket.send(cipher_text)

        # Receive return from server
        data = client_socket.recv(1024).decode()
        print(f'[Client] - Server received message: {str(data)}')

    client_socket.close()


if __name__ == '__main__':
    main()
