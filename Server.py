                              ### Mustafa Serhat USLU - 161180061 ###

                              ###  """MULTI-CLIENT CHAT SERVER""" ###

from socket import AF_INET, socket, SOCK_STREAM  #AF_INET -> address family, IPv4 | SOCK_STREAM -> TCP, connection-based
from threading import Thread

clients = {}          #Client usernames
addresses = {}        #Client addresses

HOST = '127.0.0.1'    #Localhost, establishes a loop connection with the same machine
PORT = 33000          #Communication port the application
BUFSIZ = 1024         #Message sizes
ADDR = (HOST, PORT)   #The complete TCP/IP address which will be bonded together.

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


""" HANDLES INCOMING CLIENTS """
def accept_incoming_connections():                            #Always waiting for a new connection

    while True:                                               #Sends a welcome message to the client, asks for a username
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("_______________________________ PLEASE CHOOSE A USERNAME TO START CHATTING _________________________________\n\n\n", "utf8"))
        addresses[client] = client_address                    #Saves the client address
        Thread(target=handle_client, args=(client,)).start()  #Starts handling the client actions (sending, receiving and exiting)



""" HANDLES CONNECTED CLIENTS """
def handle_client(client):                                    #Takes client socket as an argument.

    name = client.recv(BUFSIZ).decode("utf8")                 #Get client username.

    welcome = 'Welcome %s! If you want to quit, type $exit to exit.\n' % name     #Greet the client.
    client.send(bytes(welcome, "utf8"))

    msg = "@ %s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))                            #Send a message to every client to let them know about the new client.
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)                            #Receive message sent by connected client.
        if msg != bytes("$exit", "utf8"):                   #If s/he doesnt want to quit, broadcast the message to every client.
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("$exit", "utf8"))             #If wants to quit, we echo back a quit message to trigger a client side closure.
            client.close()                                   #Also disconnect the server from the client.
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break



"""SEND MESSAGES TO EVERY CLIENT"""
def broadcast(msg, prefix=""):  # prefix is the sender username of the message, the owner of the message so it can be displayed at the destination..

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)



if __name__ == "__main__":
    SERVER.listen(5)    #Able to connect to 5 clients at any time.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join() #Enables us to wait until a thread of a client is finished to start another one, this way there are no overlaps.
    SERVER.close()