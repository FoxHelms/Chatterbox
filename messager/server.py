from socket import socket as s
from socket import AF_INET, SOCK_STREAM
import logging
from concurrent.futures import ThreadPoolExecutor
import random
from time import sleep

		

class ChatServer:
	def __init__(self, host, port):
		self.logger = self._setup_logger()
		self.sock = self._setup_socket(host, port)
		self.connections = []
		self.clients = {}
		self.executor = ThreadPoolExecutor()
	
	def run(self):
		self.logger.info("Chat server is running")

		while True:
			conn, addr = self.sock.accept()
			self.executor.submit(self.client_handler, conn, addr)
		
		
	
	def client_handler(self, conn, addr):
		try: 
			temp_usernames = [username for username in self.clients.keys()]
			username = conn.recv(1024).decode('utf-8')
			self.clients[username] = conn
			self.logger.debug(f"{username} connected.")
			conn.send("Who would you like to chat with?\n".encode())
			conn.send('\n'.join(temp_usernames).encode())

			while True:
				data = conn.recv(1024).decode()
				self.logger.info(f'{addr[0]} said {data}')

				# uncommment for auto-close
				if not data:
					self.logger.warning("No data. Exiting")
					break

				if ':' in data:
					recipient, message = data.split(':', 1)
					if recipient in self.clients:
						self.clients[recipient].send(f"{username}:\n{message}".encode('utf-8'))
					else:
						conn.send(f"Error: User '{recipient}' not found.".encode('utf-8'))
				else:
					conn.send("Invalid message format. Use 'recipient:message'".encode('utf-8'))


			# Uncomment to notify everyone who is in chat
			# connected_addresses = [existing_conn.getpeername() for existing_conn in self.connections]
			# if conn not in self.connections:
			# 	welcome_message = f"\nOther users in chat:\n{connected_addresses}\n"
			# 	self.connections.append(conn)
			# 	conn.send(welcome_message.encode())
			# 	for c in self.connections:
			# 		c.send(f"{username} just joined the chat!\n".encode())
						
		except Exception as e:
			self.logger.debug(f"Error with client {addr}: {e}")
			if username in self.clients:
				del self.clients[username]
			conn.close()
			self.logger.info(f"Client {username} disconnected.")
		

			

			# recipient_opts = []
			# for conn_opt in self.connections:
			# 	if conn_opt.getpeername() != conn_opt.getsockname():
			# 		recipient_opts.append(conn_opt)
			# connection = random.choice(recipient_opts)
			# connection.send(f'{addr[0]} : \n{data.decode()}'.encode())
			# self.turns += 1
			# sleep(1)

				

	@staticmethod
	def _setup_socket(host, port):	
		sock = s(AF_INET, SOCK_STREAM)
		sock.bind((host, port))
		sock.listen(5)
		return sock
		
	@staticmethod
	def _setup_logger():
		logger = logging.getLogger('chat_server')
		logger.addHandler(logging.StreamHandler())
		logger.setLevel(logging.DEBUG)
		return logger

if __name__ == "__main__":
	server = ChatServer('localhost', 8080)
	server.run()
