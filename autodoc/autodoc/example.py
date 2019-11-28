from . import utf8
from .struct import Struct


class Example(list):
    Item = Struct.define('Item', text='', classes=None)

    def append(self, text, classes=None):
        if isinstance(classes, utf8.string):
            classes = [classes]

        list.append(self, Example.Item(text=text, classes=classes))
