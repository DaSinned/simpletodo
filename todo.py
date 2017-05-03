# -*- coding: utf-8 -*-
from db import DatabaseManager
import datetime
import re
from dateutil.parser import parse


class Todo(object):
    _db = None
    DATETIME_FORMAT = "%Y-%m-%d %H:%M"
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M"

    def __init__(self):
        self._db = DatabaseManager()

    def list(self):
        """prints out formatted entries"""
        todo_list = self.get_list()

        max_indent = len(str(todo_list[-1][0]))

        for item in todo_list:

            indent = 0
            if len(str(item[0])) < max_indent:
                indent = max_indent - len(str(item[0]))

            if item[2] == "0000-00-00 00:00:00":
                print("#{}{}: {}".format(" " * indent, item[0], item[1]))
            else:
                print("#{}{}: {} @ {}".format(" " * indent, item[0], item[1], item[2]))

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
        """parse datetime from user input

        Args:
            inp (str): user input

        Returns:
            datetime
        """

        inp = inp.lower()

        # split date input
        # (heute 19:00)|(nächste woche)|(14.04.2017 18:00)
        pattern = re.compile('^([A-Za-zäöüß]+) ([0-9:]+)|([A-Za-zäöüß ]+)|([0-9.: ]+)$')
        match = re.search(pattern, inp)

        if match.group(1) and match.group(2):
            # word + time
            print("{} {}".format(self.parse_word(match.group(1), False), match.group(2)))
            return parse("{} {}".format(self.parse_word(match.group(1), False), match.group(2)), dayfirst=True)
            pass
        if match.group(3):
            # word only
            return self.parse_word(match.group(3))
        if match.group(4):
            # date to parse
            return parse(match.group(4), dayfirst=True)

    def parse_word(self, word, time=True):
        """parse a word and try to get the date

        Args:
            word (str): input word
            time (bool): whether to show datetime or date

        Returns: 
            datetime
        """

        if time:
            _format = self.DATETIME_FORMAT
        else:
            _format = self.DATE_FORMAT

        # today
        if word.strip() == "heute":
            date = datetime.datetime.today()
            return date.strftime(_format)
        # tomorrow
        if word.strip() == "morgen":
            date = datetime.datetime.today() + datetime.timedelta(days=1)
            return date.strftime(_format)
        # next week
        if word.strip() == "nächste woche":
            date = datetime.datetime.today() + datetime.timedelta(days=7)
            return date.strftime(_format)

        raise ValueError("date word not recognized")

    def done(self, id):
        """removes entry with given id from db

        Todo: remove and add it to an archive table

        Args:
            id (int): entry id
        """

        sql = 'DELETE FROM todo WHERE id = ?'
        self._db.query(sql, [id])
