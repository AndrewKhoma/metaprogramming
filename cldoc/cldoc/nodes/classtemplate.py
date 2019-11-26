from .cclass import Class
from .cstruct import Struct
from .node import Node
from .templated import Templated
from ..clang import cindex


class StructTemplate(Struct, Templated):
    kind = None

    def __init__(self, cursor, comment):
        super(StructTemplate, self).__init__(cursor, comment)


class ClassTemplate(Class, Templated):
    kind = None

    def __init__(self, cursor, comment):
        super(ClassTemplate, self).__init__(cursor, comment)


class ClassTemplatePlexer(Node):
    kind = cindex.CursorKind.CLASS_TEMPLATE

    def __new__(cls, cursor, comment):
        # Check manually if this is actually a struct, so that we instantiate
        # the right thing. I'm not sure there is another way to do this right now
        l = list(cursor.get_tokens())

        for i in range(len(l)):
            if l[i].kind == cindex.TokenKind.PUNCTUATION and l[i].spelling == '>':
                if i < len(l) - 2:
                    if l[i + 1].kind == cindex.TokenKind.KEYWORD and \
                            l[i + 1].spelling == 'struct':
                        return StructTemplate(cursor, comment)
                break

        return ClassTemplate(cursor, comment)
