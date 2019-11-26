from .node import Node

from ..clang import cindex


class Namespace(Node):
    kind = cindex.CursorKind.NAMESPACE

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

        self.process_children = True
