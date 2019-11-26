from .ctype import Type
from .node import Node
from ..clang import cindex


class Typedef(Node):
    kind = cindex.CursorKind.TYPEDEF_DECL

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

        children = [child for child in cursor.get_children()]

        if len(children) == 1 and children[0].kind == cindex.CursorKind.TYPE_REF:
            typecursor = children[0]
        else:
            self.process_children = True
            typecursor = cursor

        self.type = Type(cursor.underlying_typedef_type, typecursor)
