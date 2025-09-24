from socket import socket as s
from socket import AF_INET, SOCK_STREAM
import logging
import random
from threading import Thread

class ChatClient:
	def __init__(self, host, port):
		self.logger = self._setup_logger()
		self.sock = self._setup_socket(host, port)

		username = input("Enter your username: ")
		self.sock.sendall(username.encode('utf-8'))
		
		thread = Thread(target=self.recv_message)
		thread.daemon = True
		thread.start()

		while True:
			message = input("> ")
			self.send_message(message)

		self.sock.close()

	def recv_message(self):
			while True:
				try:
					data = self.sock.recv(1024).decode('utf-8')
					if not data:
						break
					self.logger.info(data)
				except:
					break
	

	def send_message(self, message):
		# message = input("> ")
		bytes_sent = self.sock.send(message.encode('utf-8'))
		# self.logger.debug(f'Successfully sent {bytes_sent} bytes')

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
