from .ctype import Type
from .node import Node
from ..clang import cindex


class Field(Node):
    kind = cindex.CursorKind.FIELD_DECL

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)
        self.type = Type(cursor.type, cursor=cursor)

    def compare_same(self, other):
        return cmp(self.sort_index, other.sort_index)
