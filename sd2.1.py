import sqlite3
import os

# 1. Define a base class for NetworkDevice
class NetworkDevice:
	def __init__(self,hostname,ip_address, device_type): #Method
		self.hostname = hostnameself #Object
		self.ip_address = ip_address #Object
		self.device_type = device_type#Object

	def display_device_info(self):
		"""Display The information of the device"""
		print(f"Hostname:{self.hostname}")#Instance Variable
		print(f"IP Address:{self.ip_address}")#Instance Variable

	def to_tuple(self):
		""" Return device info as a tuple for SQL insertion"""
		return(self.hostname, self.ip_address, self.device_type)


# 2. Define a subclass for Router with additional properties
class Router(NetworkDevice):
	def __init__(self,hostname, ip_address, routing_protocol): # This is the method 
		super().__init__(hostname, ip_address, "Router") # This will activate the parent class with these attributes
		self.routing_protocol = routing_protocol #This is the instance variable

	def display_routing_info(self): # This is function 
		"""Display router-specific info"""
		print(f"Routing Protocol: {self.routing_protocol}")	# This is printing the instance variable

# 3. Define a function to handle file logging
def log_to_file(message):
	"""Logs mesages to a text file"""
	with open('network_log.txt', 'a') as log_file:
		log_file.write(message + '\n')		

#4. Exception handling for database operations
def safe_execute(cursor, query, params=())
	"""Safley execute SQL commands with error handling"""
	try:
		cursor.execute(query, params)
	except sqlite3.Error as e:
		print(f"Database error: {e}")
		log_to_file(f"Database error: {e}")
		