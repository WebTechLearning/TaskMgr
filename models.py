import os
from peewee import *

db = SqliteDatabase('task.db')

class Task(Model):
    title = CharField()
    content = TextField(null=True)
    stime = DateTimeField(null=True)
    etime = DateTimeField(null=True)
    importance = IntegerField(default=1)
    urgency = IntegerField(default=1)

    class Meta:
        database = db

if __name__ == '__main__':
    if not os.path.exists('task.db'):
        db.connect()
        db.create_tables([Task])
    task = Task(title='new task')
    task.save()
    for task in Task.select():
        print(task.title)