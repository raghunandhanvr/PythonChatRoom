#importing stuffs -- sockets and threads
#connecting to the server
#listening the broadcast and sending your name to the server to join
#receiving messages form server
#sending messages to the server
#Finally to work with everything -- we'r starting the threads to read and write 


import socket
import threading

# Choosing Nickname
nickname = input("Name: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))                            #Instead of connecting, we'r binding to the host's port(Port Number is Confidential)

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')  

            #cheching the message which is decoded to NICK and if yes were moving up!
            if message == 'NICK':                           
                client.send(nickname.encode('ascii'))    
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:  
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start() 
