from abc import *
import include.etl_exception as etl_exception
import include.log as log

class RDBMSLoader:
	def __init__(self, config, debug = True):
		self.db_connection = None
		self.debug = debug
		self.config = config

		if self.connectDB() == False:
			raise etl_exception.RDBConnectErrorException

	def __del__(self):
		self.disconnectDB()

	def setDebug(self, debug):
		self.debug = debug

	@abstractmethod
	def disconnectDB(self):
		pass

	@abstractmethod
	def connectDB(self):
		pass

	def getCursor(self):
		try:
			return self.db_connection.cursor()
		except Exception as e:
			if self.connectDB() and self.db_connection:
				return self.db_connection.cursor()
		return None

	def commit(self):
		try:
			self.db_connection.commit()
		except Exception as e:
			if self.connectDB() and self.db_connection:
				self.db_connection.commit()

	def rollback(self):
		try:
			self.db_connection.rollback()
		except Exception as e:
			if self.connectDB and self.db_connection:
				self.db_connection.rollback()
