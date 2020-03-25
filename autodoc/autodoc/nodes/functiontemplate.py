from .function import Function
from .method import Method
from .node import Node
from .templated import Templated
from ..clang import cindex


class FunctionTemplate(Templated, Function):
    kind = None

    def __init__(self, cursor, comment):
        super(FunctionTemplate, self).__init__(cursor, comment)


class MethodTemplate(Templated, Method):
    kind = None

    def __init__(self, cursor, comment):
        super(MethodTemplate, self).__init__(cursor, comment)


class FunctionTemplatePlexer(Node):
    kind = cindex.CursorKind.FUNCTION_TEMPLATE

    def __new__(cls, cursor, comment):
        if not cursor is None and (cursor.semantic_parent.kind == cindex.CursorKind.CLASS_DECL or \
                                   cursor.semantic_parent.kind == cindex.CursorKind.CLASS_TEMPLATE or \
                                   cursor.semantic_parent.kind == cindex.CursorKind.STRUCT_DECL):
            return MethodTemplate(cursor, comment)
        else:
            return FunctionTemplate(cursor, comment)
