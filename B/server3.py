
from socket import *
import _thread, base64

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 8080
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("", serverPort))

serverSocket.listen(5)
print('The server is running')	
# Server should be up and running and listening to the incoming connections


def process(connectionSocket) :	
	# Receives the request message from the client
	message = connectionSocket.recv(1024).decode()
	if len(message) > 1:
		try:
			for line in message.split('\n'):
				if line.startswith("Authorization: "):
					basic = line.split(':')[1].strip()
					auth = basic.split(' ')[1]
					username, password = base64.b64decode(auth).decode().split(':')
					print(username, password)
					if username == '17138916' and password == '17138916':
						contentType = "text/html"
						connectionSocket.send(("HTTP/1.1 200 OK\r\nContent-Type:" + contentType + "\r\n\r\n").encode())
						connectionSocket.send("Authorised. Hello Chang Liu".encode())
						connectionSocket.close()
						return
					else:
						contentType = "text/html"
						connectionSocket.send(("HTTP/1.1 401 Unauthozied\r\nContent-Type:" + contentType + "\r\n\r\n").encode())
						connectionSocket.send("401 Unauthozied due to you used a wrong or empty password. please press Ctrl + R (Command + R), then use Chang Liu's Student ID to login.".encode())
						connectionSocket.close()
						return
			contentType = "text/html"
			connectionSocket.send(("HTTP/1.1 401 Unauthozied\r\nWWW-Authenticate: Basic realm=\"Please Login\"\r\nContent-Type:" + contentType + "\r\n\r\n").encode())
			connectionSocket.send("401 Unauthozied due to you canceled login. please press Ctrl + R (Command + R), then use Chang Liu's Student ID to login.".encode())
			connectionSocket.close()
		except IOError:
			# Send HTTP response message for file not found
			print(message)
			connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
			connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
			connectionSocket.close()

while True:
	
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()
	#Clients timeout after 60 seconds of inactivity and must reconnect.
	connectionSocket.settimeout(60)
	# start new thread to handle incoming request
	_thread.start_new_thread(process,(connectionSocket,))

serverSocket.close()  



