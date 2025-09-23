from socket import socket as s
from socket import AF_INET, SOCK_STREAM
import logging
from threading import Thread

class ChatClient:
	def __init__(self, host, port):
		self.logger = self._setup_logger()
		self.sock = self._setup_socket(host, port)
	
		thread = Thread(target=self.send_message)
		thread.daemon = True
		thread.start()
		
		while True:
			data = self.sock.recv(1024)
			if not data:
				break
			self.logger.info(data.decode())
	
			

	def send_message(self):
		while True:
			message = input()
			bytes_sent = self.sock.send(message.encode())
			self.logger.debug(f'Successfully sent {bytes_sent} bytes')

	def run(self):
		self.logger.info("Chat client is running")
		while True:
			conn, addr = self.sock.accept()
			self.logger.debug(f"New connection: {addr}")

	@staticmethod
	def _setup_socket(host, port):	
		sock = s(AF_INET, SOCK_STREAM)
		sock.connect((host, port))
		return sock
		
	@staticmethod
	def _setup_logger():
		logger = logging.getLogger('chat_server')
		logger.addHandler(logging.StreamHandler())
		logger.setLevel(logging.DEBUG)
		return logger


if __name__ == "__main__":
	client = ChatClient('localhost', 8080)
