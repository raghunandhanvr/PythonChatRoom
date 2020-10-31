#we need a server sys and a client sys 

#import required stuffs which wil be sockets and threadinng
#connection
#starting the server
#adding lists -- which is client (leaving that empty so that they can add their name after joining) --- mr.robot style  ;)
#methods required for the chat  -- Ill combine all methods with a main method
##definig main receive functions -- Broadcast, handler, receiving and listining function


import socket
import threading


# Connection Data  
#Port is confidential thing
host = '127.0.0.1'                                                 #IP of your host
port = 12345                                                       #Dont take reserved ports

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #Internet socket
server.bind((host, port))                                          #Server is binded to local host and a port  
server.listen()                                                    #Server is set to listining mode

# Lists For Clients and Their Nicknames
clients = [] 
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message): 
    for client in clients:
        client.send(message)                                        #Getting all the clients and sending msg that new one joined to the admin

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)                      
            broadcast(message)                                      #After receiving we are broadcasting to other
        except:
            # Removing And Closing Clients
            index = clients.index(client)        
            clients.remove(client)       
            client.close()
            nickname = nicknames[index]                             #When we remove client we'l also remove nicknamesw with help of index
            broadcast('{} left!'.format(nickname).encode('ascii'))  
            nicknames.remove(nickname)
            break        

#These Functions will run later on in a thread so evrything will be running
#Main method receive to combine all methods


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()                          #In server IP wil login so different IP will login with same port on the server IP
        print("Connected with {}".format(str(address)))            #Waiting for the connection and accepting the connections

        #Getting nickname by asking --- code word sent the client and the client side accepts the encoded code which is NICK here and send backs the message that he can join
        #Request And Store Nickname

        client.send('NICK'.encode('ascii'))                        #Sending in encoded form 
        nickname = client.recv(1024).decode('ascii')                
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname  
        #pritning
        print("Name is {}".format(nickname))
        #broadcasting
        broadcast("{} joined!".format(nickname).encode('ascii'))   #So that every client will know new connection is joined
        client.send('Connected to server!'.encode('ascii'))        #Connected and can starting

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))   #This is because multiple client send multiple messages and so to avoid crashing we are handling with handler
        thread.start()                                             #To work with threads you need start method or run method

print("Server is started................,:) ")
receive()