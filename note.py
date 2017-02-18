from datetime import datetime

class Note:
    def __init__(self, index, context, timestamp):
        self.__index = index
        self.__context = context
        self.__timestamp = timestamp

    def __str__(self):
        return str(self.__index) + '. ' + self.__context

    @property
    def index(self):
        return self.__index

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, context):
        self.__context = context