
from socket import *
import _thread

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 8080
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("", serverPort))

serverSocket.listen(5)
print('The server is running')	
# Server should be up and running and listening to the incoming connections

def process_welcome(message, connectionSocket):
	print(message)
	for line in message.split('\n')[1:]:
		if line.startswith('Cookie:'):
			name = line.split(':')[1]
			print(name)
			name = name.split('=')[1]
			return "<html><h1>Welcome %s</h1></html>" % name
	# No cookie:
	return """<form action="/submit" method="get" >  
    Name: <input type="text" name="name" placeholder="Please enter your name"/>
    <input type="submit" value="Submit"/> 
</form>"""

def process_submit(message, connectionSocket):
	filename = message.split()[1]
	name = filename.split('?')[1].split('=')[1]
	return ("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nSet-Cookie: name=%s" % name + "\r\n\r\n").encode(), ("<html><h1>Welcome %s</h1></html>" % name).encode()

def process(connectionSocket) :	
	# Receives the request message from the client
	message = connectionSocket.recv(1024).decode()
	if len(message) > 1:
		try:
			# Extract the path of the requested object from the message
			filename = message.split()[1]

			if filename == '/welcome':
				contentType = "text/html"
				response_header = ("HTTP/1.1 200 OK\r\nContent-Type:" + contentType + "\r\n\r\n").encode()
				outputdata = process_welcome(message, connectionSocket).encode()
			elif filename.startswith('/submit?'):
				response_header, outputdata = process_submit(message, connectionSocket)
			else:
				# Because the extracted path of the HTTP request includes
				# a character '/', we read the path from the second character
				f = open(filename[1:],"rb")
				# Store the entire content of the requested file in a temporary buffer
				outputdata = f.read()
				contentType = ""
				# if the filename ends with html then set the Content-Type to be "text/html"
				if filename.endswith("html"):
					contentType = "text/html"
				# if the filename ends with (png||jpg) then set the Content-Type to be "image/(png||jpg)"
				if filename.endswith(('png', 'jpg')):
					contentType = "image/"+filename.split('.')[-1]
				response_header = ("HTTP/1.1 200 OK\r\nContent-Type:"+contentType+"\r\n\r\n").encode()

			# Send the HTTP response header line to the connection socket
			connectionSocket.send(response_header)
			# Send the content of the requested file to the connection socket
			connectionSocket.send(outputdata)
			# Close the client connection socket
			connectionSocket.close()
		except IOError:
			# Send HTTP response message for file not found
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



