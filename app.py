# -*- coding: utf-8 -*-
from todo import Todo
import sys

todo = None


def main():

    helptext = """SimpleTodo

possible commands:
    list            - shows entries
    done ID         - remove entry from database
    add TEXT @ DATE - add a new entry, '@ DATE' is optional
                      see parsedatetime documentation for date commands
    """

    try:
        if len(sys.argv) > 1:
            _action = sys.argv[1]

            if not sys.argv[1]:
                print(helptext)

            if _action == "list":
                todo.list()
            elif _action == "add":
                todo.add(" ".join(sys.argv[2:]))
                todo.list()
            elif _action == "done":
                todo.done(sys.argv[2])
                todo.list()
            else:
                print(helptext)
        else:
            print(helptext)

    except Exception as e:
        print(helptext)
        print("Error: {}".format(e))


if __name__ == '__main__':
    todo = Todo()
    main()
