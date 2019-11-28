from .ctype import Type
from .node import Node
from ..clang import cindex


class Variable(Node):
    kind = cindex.CursorKind.VAR_DECL

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

        self.type = Type(cursor.type, cursor=cursor)
