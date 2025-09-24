import socket

HOST = 'test-server'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	s.sendall(b'Hello, server')
	data = s.recv(1024)
print('Received: {data.decode()}')
