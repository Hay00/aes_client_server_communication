from Crypto.Cipher import AES


def encrypt(key, msg):
    cipher = AES.new(key, AES.MODE_EAX, nonce=key)
    nonce = cipher.nonce
    cipher_text, tag = cipher.encrypt_and_digest(msg.encode('UTF-8'))
    return nonce, cipher_text, tag


def decrypt(key, nonce, cipher_text, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(cipher_text)
    try:
        cipher.verify(tag)
        return plaintext.decode('UTF-8')
    except ValueError:
        return False
