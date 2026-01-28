import mysql.connector
import include.etl_exception as etl_exception
import include.log as log
from include.rdbms_db_loader import RDBMSLoader

class MySQLDBLoader(RDBMSLoader):
	def __init__(self, config, debug = True):
		super().__init__(config, debug)

	def disconnectDB(self):
		try:
			if self.db_connection and self.db_connection.is_connected():
				self.db_connection.close()
			log.printLog('DB Disconnect Success')
		except Exception as e:
			log.printException()

	def connectDB(self):
		try:
			if not self.db_connection or self.db_connection.is_connected() == False:
				log.printLog("DB Connect Start")				
				host = self.config.get('host', self.config.get('HOST', ''))
				server = self.config.get('server', self.config.get('SERVER', ''))
				port = self.config.get('port', self.config.get('PORT', ''))

				if host:
					try:
						server, port = host.split(":")
					except Exception as e:
						server = host
						port = 3306

				user = self.config.get('id', self.config.get('ID', ''))
				password = self.config.get('password', self.config.get('PASSWORD', ''))
				database = self.config.get('db_name', self.config.get('DB_NAME', ''))
				
				# log.printLog(self.config)
				# log.printLog(server, port, user, password, database)
				self.db_connection = mysql.connector.connect(host=server, user=user, password=password, database=database, port=port, charset="utf8mb4", use_unicode=True, auth_plugin='mysql_native_password')
				if self.debug :
					log.printLog("DB Connect Success")
			return True
		except mysql.connector.Error as e:
			if e.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
				log.printException("Something is wrong with your name or password")
			elif e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
				log.printException("Database does not exist")
			else:
				log.printException(e)
		except Exception as e:
			log.printException(exit_program=True)
		return False