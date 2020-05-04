                              ### Mustafa Serhat USLU - 161180061 ###

                                 ###  """CLIENT AND GUI""" ###

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


HOST = "127.0.0.1"     #Localhost, establishes a loop connection with the same machine, which hosts the server.
PORT =  33000          #Communication port the application
BUFSIZ = 1024          #Message sizes
ADDR = (HOST, PORT)    #The complete TCP/IP address which will be bonded together.

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


"""HANDLES RECEIVING OF MESSAGES"""
def receive():
    while True:                                                       #Always looking for messages to receive.
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")           #Get message, if there is one.

            separated_msg = msg.split(maxsplit=2)
            if separated_msg[0] == '@':
                joinened_clients_list.insert(tkinter.END, separated_msg[1])
                msg = separated_msg[1] + separated_msg[2]


            msg_list.insert(tkinter.END, msg)                         #Insert the received message to GUI window.
        except OSError:                                               #Client has left the chat.
            break


"""HANDLES SENDING OF MESSAGES"""
def send(event=None):                                                 #event is connected to the "send" button on the UI.
    msg = my_msg.get()
    my_msg.set("")                                                    #Clears input field in UI after receiving.
    client_socket.send(bytes(msg, "utf8"))                            #Send message through our connection.
    if msg == "$exit":                                                #$exit is for exiting the UI window.
        client_socket.close()
        top.quit()                                                    #(top is our GUI window)


"""CLOSES THE GUI WINDOW WHEN X IS PRESSED ON THE WINDOW"""
def on_closing(event=None):
    my_msg.set("$exit")
    send()                                                            #Send quit command to the server and close client.



"""GUI CONSTRUCTION SECTION"""
top = tkinter.Tk()                                                     #top  is our GUI window (Highest level of frame)
top.title("Gazi_University_Chat")

#SCROLLBAR
scrollbar = tkinter.Scrollbar(top)                                     #To navigate through all messages.

#PLACE TO CONTAIN ALL MESSAGES
msg_list = tkinter.Listbox(top, height=18, width=100, yscrollcommand=scrollbar.set)

#PLACE TO CONTAIN JOINED MEMBER NAMES
joinened_clients_list = tkinter.Listbox(top, height=8, width=22)
joinened_clients_list.insert(tkinter.END, "GROUP MEMBERS:")

#TEXT ENTRY BOX TO SEND MSG
my_msg = tkinter.StringVar()                                           #For the messages which will be sent.
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)                                     #We bind the enter key with the send function.

#LABELS
Label_1 = tkinter.Label(top, text="Enter your messages here")

#SEND BUTTON
send_button = tkinter.Button(top, text="Send", command=send)

#PLACEMENTS OF THE WIDGETS
scrollbar.grid(row=0, column=1, sticky='ns')
msg_list.grid(row=0, column=0)
Label_1.grid(row=1, column=0)
entry_field.grid(row=2, column=0)
send_button.grid(row=3, column=0)
joinened_clients_list.grid(row=0, column=2, sticky='n')


#LET SERVER KNOW THAT CLIENT IS GONE WHEN TOP RIGHT 'X' IS CLICKED (works by calling "on_closing" function).
top.protocol("WM_DELETE_WINDOW", on_closing)                          #Enables us to send the server {quit message}.



"""START A THREAD TO ALWAYS LOOK FOR MESSAGES TO GET"""
receive_thread = Thread(target=receive)
receive_thread.start()

tkinter.mainloop()  # Starts GUI execution.