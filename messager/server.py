from socket import socket as s
from socket import AF_INET, SOCK_STREAM
import logging
from concurrent.futures import ThreadPoolExecutor

class Conversation:
	def __init__(self):
		self.parties = {}

	def add_party(self, address):
		self.parties[address] = 0
		

class ChatServer:
	def __init__(self, host, port):
		self.logger = self._setup_logger()
		self.sock = self._setup_socket(host, port)
		self.connections = []
		self.conversations = []
		self.executor = ThreadPoolExecutor()
	
	def run(self):
		self.logger.info("Chat server is running")
		while True:
			conn, addr = self.sock.accept()
			self.logger.debug(f"New connection: {addr}")
			new_connection_alert = f"{addr} just joined the chat!"
			connected_addresses = []
			for existing_conn in self.connections:
				existing_conn.send(new_connection_alert.encode())
				connected_addresses.append(existing_conn.getsockname()[0])			

			welcome_message = f"\nOther users in chat:\n{connected_addresses}"
			if len(self.connections) == 0:
				welcome_message = "You're the only person online. Wait for someone to join"
			conn.send(welcome_message.encode())
			self.connections.append(conn)
			self.logger.debug(f"Connections: {self.connections}")
			self.executor.submit(self.relay_messages, conn, addr)
			

	def relay_messages(self, conn, addr):
		while True:
			data = conn.recv(1024)

			self.logger.debug(f'{addr[0]} said {data.decode()}')


			for connection in self.connections:
				connection.send(f'{addr[0]} : \n{data.decode()}'.encode())

			if not data:
				self.logger.warning("No data. Exiting")
				break		

	@staticmethod
	def _setup_socket(host, port):	
		sock = s(AF_INET, SOCK_STREAM)
		sock.bind((host, port))
		sock.listen()
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
