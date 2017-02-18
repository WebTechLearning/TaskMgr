from task import Task
from note import Note

import argparse

parser = argparse.ArgumentParser(prog = 'taskMgr',
                                 description = 'A prioritization based task manager')
subparsers = parser.add_subparsers()

""">>> taskMgr new <title> <description>"""
cmdNew = subparsers.add_parser('new')
cmdNew.add_argument('title', nargs = 1, type = str)
cmdNew.add_argument('description', nargs = 1, type = str)

""">>> taskMgr remove <title>"""
cmdRemove = subparsers.add_parser('remove')
cmdRemove.add_argument('title', nargs = 1, type = str)

""">>> taskMgr move <title> -to <class>"""
cmdMove = subparsers.add_parser('move')
cmdMove.add_argument('title', nargs = 1, type = str)
cmdMove.add_argument('-to', choices = ['todo', 'week', 'today'])

""">>> taskMgr show"""
cmdShow = subparsers.add_parser('show')

# TEST
args = parser.parse_args(['new', 'AP-12345', 'The first JIRA'])
print(args.title, args.description)
args = parser.parse_args(['remove', 'AP-12345'])
print(args.title)
args = parser.parse_args(['move', 'AP-12345', '-to', 'today'])
print(args.title, args.to)