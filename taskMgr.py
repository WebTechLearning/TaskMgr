import sqlite3
from contextlib import contextmanager

class Sqlite3Interphase:
    def __init__(self, db):
        self.__db = db

    def Connect(self):
        self.__connect = sqlite3.connect(self.__db)
        self.__cursor = self.__connect.cursor()

    def Close(self):
        self.__connect.close()

    def Commit(self):
        self.__connect.commit()

    def CommitAndClose(self):
        self.__connect.commit()
        self.__connect.close()

    @property
    def cursor(self):
        return self.__cursor

class TaskTable(Sqlite3Interphase):
    def __init__(self):
        super().__init__('taskDB')

    @contextmanager
    def TableChange(self):
        yield
        self.Commit()

    def CreateTable(self):
        with self.TableChange():
            self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS tasks
            (title text primary key, tag text, context text, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    def New(self, title, context):
        with self.TableChange():
            self.cursor.execute('INSERT OR IGNORE INTO tasks(title, tag, context) VALUES (?, ?, ?)', (title, 'TODO', context))

    def Delete(self, title):
        with self.TableChange():
            self.cursor.execute('DELETE FROM tasks WHERE title=\'' + title + '\'')

    def Move(self, title, toTag):
        with self.TableChange():
            self.cursor.execute('UPDATE tasks SET tag=\'' + toTag + '\' WHERE title=\'' + title + '\'')

    def Fetch(self, tag):
        return self.cursor.execute('SELECT * FROM tasks WHERE tag=\'' + tag + '\'')

class TaskMgr:
    def __init__(self):
        self.__taskTable = TaskTable()
        self.__taskTable.Connect()
        self.__taskTable.CreateTable()
        self.TAGS = ['TODAY', 'WEEK', 'TODO']
    def __del__(self):
        self.__taskTable.CommitAndClose()

    @contextmanager
    def CmdContext(self, cmd):
        print('BEGIN taskMgr.' + cmd)
        yield
        print('END taskMgr.' + cmd)

    def New(self, args):
        with self.CmdContext('New'):
            self.__taskTable.New(args.title[0], args.context[0])

    def Remove(self, args):
        with self.CmdContext('Remove'):
            self.__taskTable.Delete(args.title[0])

    def Move(self, args):
        with self.CmdContext('Move'):
            self.__taskTable.Move(args.title[0], args.to.upper())

    def Show(self, args):
        with self.CmdContext('Show'):
            for tag in self.TAGS:
                print('----', tag, '----')
                tasks = self.__taskTable.Fetch(tag)
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