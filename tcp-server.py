import socket 

def close_connections():
# Closing all Connections 
    for conn in connections:
        conn[0].close()


if __name__ == '__main__': 
	
    # Defining Socket 
    host = '192.168.1.104' #ip de la caja
    port = 8080
    totalclient = int(input('Enter number of clients: ')) 

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.bind((host,port)) 
    sock.listen(totalclient) 
	# Establishing Connections 
    connections = [] 
    print('Initiating clients') 
    for i in range(totalclient): 
        conn = sock.accept() 
        connections.append(conn) 
        print('Connected with client', i+1) 

    fileno = 0
    idx = 0
    for conn in connections: 
        # Receiving File Data 
        idx += 1
        data = conn[0].recv(1024).decode('utf-8') 

        if not data: 
            continue
	   
        while data:
    # Creating a new file at server end and writing the data 
            fileno = fileno+1
            filename = 'output'+str(fileno)+'.txt'

            fo = open(filename, "w") 
        #while data: 
           # if not data: 
                #   break
            #else: 
            fo.write(data) 
            data = conn[0].recv(1024).decode('utf-8') 
            fo.close()
            print() 
            #print('Receiving file from client', idx) 
            #print() 
            print('Received successfully! New filename is:', filename) 

            #print("recibido")
            #close_connections()
