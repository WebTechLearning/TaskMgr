from datetime import datetime

class Task:
    def __init__(self, index, title, context, timestamp):
        self.__index = index
        self.__title = title
        self.__context = context
        self.__timestamp = timestamp

    def __str__(self):
        return '('+self.__title+') ' + self.__context

    @property
    def index(self):
        return self.__index

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, context):
        self.__context = context

    @property
    def timestamp(self):
        return self.__timestamp