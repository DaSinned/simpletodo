# -*- coding: utf-8 -*-
from db import DatabaseManager
import datetime
import re
import parsedatetime


class Todo(object):
    _db = None
    _pdt = None

    LOCALE = "de_DE"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M"
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M"

    def __init__(self):
        self._db = DatabaseManager()
        self._pdt = parsedatetime.Calendar(parsedatetime.Constants(self.LOCALE))

    def list(self):
        """prints out formatted entries"""
        todo_list = self.get_list()

        if todo_list:

            max_indent = len(str(todo_list[-1][0]))

            for item in todo_list:

                indent = 0
                if len(str(item[0])) < max_indent:
                    indent = max_indent - len(str(item[0]))

                if item[2] == "0000-00-00 00:00:00":
                    print("#{}{}: {}".format(" " * indent, item[0], item[1]))
                else:
                    print("#{}{}: {} @ {}".format(" " * indent, item[0], item[1], item[2]))
        else:
            print("no tasks found")

    def get_list(self):
        """get all database entries

        Returns: 
            list of all entries
        """
        todo_list = []

        for row in self._db.query("SELECT id, title, remember FROM todo", []):
            todo_list.append(row)

        return todo_list

    def add(self, text):
        """parse user input and add to db

        Args:
            text (str): user input
        """
        if not text:
            raise Exception("empty task not allowed")

        pattern = re.compile('^(.+) @ (.+)$')
        matches = re.search(pattern, text)

        if matches:
            add_dict = {'title': matches.group(1), 'remember': self.parse_date(matches.group(2))}
        else:
            add_dict = {'title': text}

        if(add_dict):
            self.insert_todo(add_dict)

    def insert_todo(self, values):
        """insert todo dict to db

        Args:
            values (dict)
        """
        columns = ', '.join(values.keys())
        placeholders = ':' + ', :'.join(values.keys())
        sql = 'INSERT INTO todo ({}) VALUES ({})'.format(columns, placeholders)
        self._db.query(sql, values)

    def parse_date(self, inp):
        time_struct, parse_status = self._pdt.parse(inp)

        if(parse_status > 0):
            date = datetime.datetime(*time_struct[:6])
            return date.strftime(self.DATETIME_FORMAT)
        else:
            raise ValueError("date could not be parsed")

    def done(self, id):
        """removes entry with given id from db

        Todo: remove and add it to an archive table

        Args:
            id (int): entry id
        """

        sql = 'DELETE FROM todo WHERE id = ?'
        self._db.query(sql, [id])
