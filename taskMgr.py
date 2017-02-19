import sqlite3
from contextlib import contextmanager
from task import Task
# from note import Note

class Sqlite3Interphase:
    def __init__(self, db):
        self.__db = db

    def Connect(self):
        self.__connect = sqlite3.connect(self.__db)
        self.__cursor = self.__connect.cursor()

    def CommitAndClose(self):
        self.__connect.commit()
        self.__connect.close()

    @property
    def cursor(self):
        return self.__cursor

class TaskMgr:
    def __init__(self):
        self.__db = Sqlite3Interphase('taskDB')
        self.TAGS = ['TODAY', 'WEEK', 'TODO']
        self.__db.Connect()
        self.__db.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS tasks
            (title text primary key, tag text, context text, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        self.__db.CommitAndClose()

    @contextmanager
    def DbChange(self):
        self.__db.Connect()
        yield
        self.__db.CommitAndClose()

    @contextmanager
    def CmdContext(self, cmd):
        print('BEGIN taskMgr.' + cmd)
        yield
        print('END taskMgr.' + cmd)

    def New(self, args):
        with self.CmdContext('New'):
            with self.DbChange():
                self.__db.cursor.execute('INSERT INTO tasks(title, tag, context) VALUES (?, ?, ?)', (args.title[0], 'TODO', args.context[0]))

    def Remove(self, args):
        with self.CmdContext('Remove'):
            with self.DbChange():
                self.__db.cursor.execute('DELETE FROM tasks WHERE title=\'' + args.title[0] + '\'')

    def Move(self, args):
        with self.CmdContext('Move'):
            with self.DbChange():
                self.__db.cursor.execute('UPDATE tasks SET tag=\'' + args.to.upper() + '\' WHERE title=\'' + args.title[0] + '\'')

    def Show(self, args):
        with self.CmdContext('Show'):
            with self.DbChange():
                for tag in self.TAGS:
                    print('----', tag, '----')
                    tasks = self.__db.cursor.execute('SELECT * FROM tasks WHERE tag=\'' + tag + '\'')
                    for task in tasks:
                        print(' '.join(task))



taskMgr = TaskMgr()

import argparse

parser = argparse.ArgumentParser(prog = 'taskMgr',
                                 description = 'A prioritization based task manager')
subparsers = parser.add_subparsers()

""">>> taskMgr new <title> <description>"""
cmdNew = subparsers.add_parser('new')
cmdNew.add_argument('title', nargs = 1, type = str)
cmdNew.add_argument('context', nargs = 1, type = str)
cmdNew.set_defaults(func = taskMgr.New)

""">>> taskMgr remove <title>"""
cmdRemove = subparsers.add_parser('remove')
cmdRemove.add_argument('title', nargs = 1, type = str)
cmdRemove.set_defaults(func = taskMgr.Remove)

""">>> taskMgr move <title> -to <class>"""
cmdMove = subparsers.add_parser('move')
cmdMove.add_argument('title', nargs = 1, type = str)
cmdMove.add_argument('-to', choices = ['todo', 'week', 'today'])
cmdMove.set_defaults(func = taskMgr.Move)

""">>> taskMgr show"""
cmdShow = subparsers.add_parser('show')
cmdShow.set_defaults(func = taskMgr.Show)

# TEST
args = parser.parse_args(['new', 'AP-1', 'AP-1 context'])
args.func(args)
args = parser.parse_args(['new', 'AP-2', 'AP-2 context'])
args.func(args)
args = parser.parse_args(['new', 'AP-3', 'AP-3 context'])
args.func(args)
args = parser.parse_args(['remove', 'AP-3'])
args.func(args)
args = parser.parse_args(['move', 'AP-1', '-to', 'today'])
args.func(args)
args = parser.parse_args(['move', 'AP-2', '-to', 'week'])
args.func(args)
args = parser.parse_args(['show'])
args.func(args)