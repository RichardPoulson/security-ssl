"""
    client.py - Connect to an SSL server

    CSCI 3403
    Authors: Matt Niemiec and Abigail Fernandes
    Number of lines of code in solution: 117
        (Feel free to use more or less, this
        is provided as a sanity check)

    Put your team members' names:



"""

import socket
import Crypto
import base64
import os

iv = "G4XO4L\X<J;MPPLD"

host = "localhost"
port = 10001


# A helper function that you may find useful for AES encryption
def pad_message(message):
    return message + " "*((16-len(message))%16)


# TODO: Generate a random AES key
def generate_key():
    return os.urandom(16)


# TODO: Takes an AES session key and encrypts it using the server's
# TODO: public key and returns the value
def encrypt_handshake(session_key):
    with open('sshkeys.txt.pub', 'r') as file:
        serverPubKey = file.read()
    salt = 'F'
    pubkeyObj = RSA.importKey(serverPubKey)
    encryMessage = pubkeyObj.encrypt(session_key, salt)[0]
    return encryMessage


# TODO: Encrypts the message using AES. Same as server function
def encrypt_message(message, session_key):
    message = pad_message(message)
    cipertext = AES.new(session_key, AES.MODE_cCBC, iv)
    return base64.b64encode(iv + cipher.encrypt(message))


# TODO: Decrypts the message using AES. Same as server function
def decrypt_message(message, session_key):
    message = base64.b64decode(message)
    cipher = AES.new(session_key, AES.MODE_CFB, iv)
    msg = iv + cipher.decrypt(client_message)
    return msg


# Sends a message over TCP
def send_message(sock, message):
    sock.sendall(message)


# Receive a message from TCP
def receive_message(sock):
    data = sock.recv(1024)
    return data


def main():
    user = input("What's your username? ")
    password = input("What's your password? ")

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (host, port)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:
        # Message that we need to send
        message = user + ' ' + password
        # TODO: Generate random AES key
        key = generate_key()
        # TODO: Encrypt the session key using server's public key
        ekey = encrypt_handshake(key)
        # TODO: Initiate handshake
        send_message(sock, ekey)
        # Listen for okay from server (why is this necessary?)
        if receive_message(sock).decode() != "okay":
            print("Couldn't connect to server")
            exit(0)

        # TODO: Encrypt message and send to server
        send_message(sock, encrypt_message(message, key))
        # TODO: Receive and decrypt response from server and print
        msg = decrypt_message(receive_message(sock).decode(), key)
        print(msg)
    finally:
        print('closing socket')
        sock.close()


if __name__ in "__main__":
    main()
