# -*- coding: utf-8 -*-

import sqlite3

class DatabaseManager(object):
	_db_connection = None
	_db_cur = None
	_db_file = 'todo.db'

	def __init__(self):
		self._db_connection = sqlite3.connect(self._db_file)
		self._db_cur = self._db_connection.cursor()

	def query(self, query, values):
		self._db_cur.execute(query, values)
		self._db_connection.commit()
		return self._db_cur

	def __del__(self):
		self._db_connection.close()
